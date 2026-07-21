import random

from django.core.management.base import BaseCommand

from accounts.models import DealerProfile, User
from vehicles.models import Vehicle


DEMO_VEHICLES = [
    dict(make="Mercedes-Benz", model="G63 AMG", year=2023, price=178000, condition="new",
         body_style="suv", fuel_type="petrol", transmission="automatic", drivetrain="awd",
         mileage=1200, horsepower=577, engine="4.0L Twin-Turbo V8", exterior_color="Black",
         country="United States", city="Miami", is_featured=True, is_luxury=True),
    dict(make="Porsche", model="911 Turbo S", year=2022, price=215000, condition="used",
         body_style="coupe", fuel_type="petrol", transmission="automatic", drivetrain="awd",
         mileage=4500, horsepower=640, engine="3.8L Twin-Turbo Flat-6", exterior_color="Silver",
         country="Germany", city="Munich", is_featured=True, is_luxury=True),
    dict(make="Tesla", model="Model S Plaid", year=2024, price=94990, condition="new",
         body_style="sedan", fuel_type="electric", transmission="automatic", drivetrain="awd",
         mileage=50, horsepower=1020, engine="Tri-Motor Electric", exterior_color="White",
         country="United States", city="Los Angeles", is_featured=True, is_electric_collection=True),
    dict(make="BMW", model="X7 M60i", year=2023, price=98500, condition="certified",
         body_style="suv", fuel_type="petrol", transmission="automatic", drivetrain="awd",
         mileage=8200, horsepower=523, engine="4.4L Twin-Turbo V8", exterior_color="Blue",
         country="United Arab Emirates", city="Dubai"),
    dict(make="Toyota", model="Camry", year=2022, price=24500, condition="used",
         body_style="sedan", fuel_type="hybrid", transmission="automatic", drivetrain="fwd",
         mileage=18500, horsepower=208, engine="2.5L Hybrid I4", exterior_color="Grey",
         country="United States", city="Dallas"),
    dict(make="Range Rover", model="Sport Autobiography", year=2023, price=126000, condition="new",
         body_style="suv", fuel_type="petrol", transmission="automatic", drivetrain="4wd",
         mileage=300, horsepower=523, engine="4.4L Twin-Turbo V8", exterior_color="White",
         country="United Kingdom", city="London", is_luxury=True),
    dict(make="Ferrari", model="Roma", year=2023, price=245000, condition="new",
         body_style="coupe", fuel_type="petrol", transmission="automatic", drivetrain="rwd",
         mileage=600, horsepower=612, engine="3.9L Twin-Turbo V8", exterior_color="Red",
         country="Italy", city="Maranello", is_featured=True, is_luxury=True),
    dict(make="Audi", model="e-tron GT", year=2023, price=104900, condition="new",
         body_style="sedan", fuel_type="electric", transmission="automatic", drivetrain="awd",
         mileage=1500, horsepower=637, engine="Dual-Motor Electric", exterior_color="Grey",
         country="Germany", city="Ingolstadt", is_electric_collection=True),
]


class Command(BaseCommand):
    help = "Seeds demo dealer accounts and vehicle listings so the marketplace isn't empty on first run."

    def handle(self, *args, **options):
        dealer, created = User.objects.get_or_create(
            username="demo_dealer",
            defaults=dict(email="dealer@veloramotors.com", role=User.Role.DEALER),
        )
        if created:
            dealer.set_password("VeloraDemo123!")
            dealer.save()
            self.stdout.write(self.style.SUCCESS("Created demo_dealer / VeloraDemo123!"))

        DealerProfile.objects.get_or_create(
            user=dealer,
            defaults=dict(
                company_name="Velora Certified Motors",
                city="Miami", country="United States",
                is_verified=True, quality_score=96,
                description="Flagship demo dealership for the Velora Motors platform.",
            ),
        )

        created_count = 0
        for data in DEMO_VEHICLES:
            _, was_created = Vehicle.objects.get_or_create(
                dealer=dealer, make=data["make"], model=data["model"], year=data["year"],
                defaults={**data, "currency": "USD"},
            )
            created_count += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete. {created_count} new vehicles added (demo_dealer login: demo_dealer / VeloraDemo123!)."
        ))
