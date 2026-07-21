from django.contrib import messages
from django.shortcuts import redirect, render

from vehicles.models import Vehicle


def home(request):
    featured = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE, is_featured=True)[:8]
    luxury = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE, is_luxury=True)[:8]
    electric = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE, fuel_type=Vehicle.FuelType.ELECTRIC)[:8]
    suvs = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE, body_style=Vehicle.BodyStyle.SUV)[:8]
    certified = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE, condition=Vehicle.Condition.CERTIFIED)[:8]

    stats = {
        "vehicles_listed": Vehicle.objects.count(),
        "countries_served": Vehicle.objects.values("country").distinct().count() or 1,
        "avg_response_minutes": 5,
    }

    return render(request, "core/home.html", {
        "featured": featured,
        "luxury": luxury,
        "electric": electric,
        "suvs": suvs,
        "certified": certified,
        "stats": stats,
    })


def contact(request):
    if request.method == "POST":
        # Milestone 1: acknowledge submission. Wire this up to email/CRM
        # (or a Ticket model) in the next pass.
        messages.success(request, "Thanks for reaching out — our team will respond within 5 minutes during support hours.")
        return redirect("core:contact")
    return render(request, "core/contact.html")
