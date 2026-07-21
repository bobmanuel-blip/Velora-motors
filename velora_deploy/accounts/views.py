from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from vehicles.models import Vehicle, Wishlist
from .forms import DealerProfileForm, RegisterForm
from .models import DealerProfile


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            if user.is_dealer:
                DealerProfile.objects.get_or_create(
                    user=user, defaults={"company_name": f"{user.username}'s Dealership"}
                )
                messages.success(request, "Welcome to Velora Motors! Complete your dealer profile to start listing vehicles.")
                return redirect("accounts:dealer_dashboard")
            messages.success(request, "Welcome to Velora Motors!")
            return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dealer_dashboard(request):
    if not request.user.is_dealer:
        messages.error(request, "That page is only available to dealer accounts.")
        return redirect("core:home")

    profile, _ = DealerProfile.objects.get_or_create(
        user=request.user, defaults={"company_name": f"{request.user.username}'s Dealership"}
    )
    vehicles = Vehicle.objects.filter(dealer=request.user).order_by("-created_at")

    stats = {
        "total_listings": vehicles.count(),
        "available": vehicles.filter(status=Vehicle.Status.AVAILABLE).count(),
        "sold": vehicles.filter(status=Vehicle.Status.SOLD).count(),
        "featured": vehicles.filter(is_featured=True).count(),
    }

    if request.method == "POST":
        form = DealerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Dealer profile updated.")
            return redirect("accounts:dealer_dashboard")
    else:
        form = DealerProfileForm(instance=profile)

    return render(request, "accounts/dealer_dashboard.html", {
        "profile": profile,
        "vehicles": vehicles,
        "stats": stats,
        "form": form,
    })


@login_required
def buyer_dashboard(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related("vehicle")
    return render(request, "accounts/buyer_dashboard.html", {"wishlist": wishlist})
