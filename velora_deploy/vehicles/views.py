from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from .ai_search import parse_natural_query
from .forms import VehicleForm, VehicleImageFormSet
from .models import SavedSearch, Vehicle, Wishlist


def _apply_filters(qs, params: dict):
    if make := params.get("make"):
        qs = qs.filter(make__icontains=make)
    if model := params.get("model"):
        qs = qs.filter(model__icontains=model)
    if year := params.get("year"):
        qs = qs.filter(year=year)
    if price_min := params.get("price_min"):
        qs = qs.filter(price__gte=price_min)
    if price_max := params.get("price_max"):
        qs = qs.filter(price__lte=price_max)
    if country := params.get("country"):
        qs = qs.filter(country__icontains=country)
    if mileage_max := params.get("mileage_max"):
        qs = qs.filter(mileage__lte=mileage_max)
    if fuel_type := params.get("fuel_type"):
        qs = qs.filter(fuel_type=fuel_type)
    if transmission := params.get("transmission"):
        qs = qs.filter(transmission=transmission)
    if drivetrain := params.get("drivetrain"):
        qs = qs.filter(drivetrain=drivetrain)
    if body_style := params.get("body_style"):
        qs = qs.filter(body_style=body_style)
    if condition := params.get("condition"):
        qs = qs.filter(condition=condition)
    if exterior_color := params.get("exterior_color"):
        qs = qs.filter(exterior_color__icontains=exterior_color)
    return qs


def vehicle_list(request):
    qs = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE).select_related("dealer").prefetch_related("images")

    ai_query = request.GET.get("q", "").strip()
    ai_parsed = {}
    if ai_query:
        ai_parsed = parse_natural_query(ai_query)
        qs = _apply_filters(qs, ai_parsed)

    # Explicit filter form fields take precedence / add to the AI-parsed ones
    filters = {
        "make": request.GET.get("make", ""),
        "model": request.GET.get("model", ""),
        "year": request.GET.get("year", ""),
        "price_min": request.GET.get("price_min", ""),
        "price_max": request.GET.get("price_max", ""),
        "country": request.GET.get("country", ""),
        "mileage_max": request.GET.get("mileage_max", ""),
        "fuel_type": request.GET.get("fuel_type", ""),
        "transmission": request.GET.get("transmission", ""),
        "drivetrain": request.GET.get("drivetrain", ""),
        "body_style": request.GET.get("body_style", ""),
        "condition": request.GET.get("condition", ""),
    }
    active_filters = {k: v for k, v in filters.items() if v}
    qs = _apply_filters(qs, active_filters)

    sort = request.GET.get("sort", "-created_at")
    if sort in {"price", "-price", "-created_at", "mileage", "-year"}:
        qs = qs.order_by(sort)

    paginator = Paginator(qs.distinct(), 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    if request.user.is_authenticated and ai_query:
        SavedSearch.objects.get_or_create(
            user=request.user, query_params=request.GET.urlencode(),
            defaults={"label": ai_query[:150]},
        )

    return render(request, "vehicles/vehicle_list.html", {
        "page_obj": page_obj,
        "filters": filters,
        "ai_query": ai_query,
        "ai_parsed": ai_parsed,
        "condition_choices": Vehicle.Condition.choices,
        "fuel_choices": Vehicle.FuelType.choices,
        "transmission_choices": Vehicle.Transmission.choices,
        "drivetrain_choices": Vehicle.Drivetrain.choices,
        "body_style_choices": Vehicle.BodyStyle.choices,
    })


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle.objects.select_related("dealer", "dealer__dealer_profile"), pk=pk)
    Vehicle.objects.filter(pk=pk).update(view_count=F("view_count") + 1)

    is_wishlisted = (
        request.user.is_authenticated
        and Wishlist.objects.filter(user=request.user, vehicle=vehicle).exists()
    )
    similar = (
        Vehicle.objects.filter(make=vehicle.make, status=Vehicle.Status.AVAILABLE)
        .exclude(pk=vehicle.pk)[:4]
    )

    recently_viewed_ids = request.session.get("recently_viewed", [])
    if vehicle.pk in recently_viewed_ids:
        recently_viewed_ids.remove(vehicle.pk)
    recently_viewed_ids.insert(0, vehicle.pk)
    request.session["recently_viewed"] = recently_viewed_ids[:8]

    return render(request, "vehicles/vehicle_detail.html", {
        "vehicle": vehicle,
        "is_wishlisted": is_wishlisted,
        "similar": similar,
    })


@login_required
def wishlist_toggle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    obj, created = Wishlist.objects.get_or_create(user=request.user, vehicle=vehicle)
    if not created:
        obj.delete()
        messages.info(request, "Removed from your wishlist.")
    else:
        messages.success(request, "Saved to your wishlist.")
    return redirect("vehicles:vehicle_detail", pk=pk)


def compare_vehicles(request):
    ids = request.GET.getlist("id")
    vehicles = Vehicle.objects.filter(pk__in=ids).prefetch_related("images")
    return render(request, "vehicles/compare.html", {"vehicles": vehicles})


@login_required
def dealer_vehicle_create(request):
    if not request.user.is_dealer:
        messages.error(request, "Only dealer accounts can list vehicles.")
        return redirect("core:home")

    if request.method == "POST":
        form = VehicleForm(request.POST)
        formset = VehicleImageFormSet(request.POST, request.FILES, queryset=Vehicle.objects.none())
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.dealer = request.user
            vehicle.save()
            for f in request.FILES.getlist("images"):
                vehicle.images.create(image=f)
            messages.success(request, "Vehicle listed successfully.")
            return redirect("vehicles:vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm()

    return render(request, "vehicles/vehicle_form.html", {"form": form, "mode": "create"})


@login_required
def dealer_vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, dealer=request.user)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            for f in request.FILES.getlist("images"):
                vehicle.images.create(image=f)
            messages.success(request, "Vehicle updated.")
            return redirect("vehicles:vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, "vehicles/vehicle_form.html", {"form": form, "mode": "edit", "vehicle": vehicle})


@login_required
def dealer_vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, dealer=request.user)
    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Vehicle removed from your inventory.")
        return redirect("accounts:dealer_dashboard")
    return render(request, "vehicles/vehicle_confirm_delete.html", {"vehicle": vehicle})
