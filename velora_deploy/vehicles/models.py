from django.conf import settings
from django.db import models
from django.urls import reverse


class Vehicle(models.Model):
    class Condition(models.TextChoices):
        NEW = "new", "New"
        USED = "used", "Used"
        CERTIFIED = "certified", "Certified Pre-Owned"

    class FuelType(models.TextChoices):
        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        ELECTRIC = "electric", "Electric"
        HYBRID = "hybrid", "Hybrid"

    class Transmission(models.TextChoices):
        AUTOMATIC = "automatic", "Automatic"
        MANUAL = "manual", "Manual"

    class Drivetrain(models.TextChoices):
        FWD = "fwd", "Front-Wheel Drive"
        RWD = "rwd", "Rear-Wheel Drive"
        AWD = "awd", "All-Wheel Drive"
        FOUR_WD = "4wd", "Four-Wheel Drive"

    class BodyStyle(models.TextChoices):
        SEDAN = "sedan", "Sedan"
        SUV = "suv", "SUV"
        COUPE = "coupe", "Coupe"
        CONVERTIBLE = "convertible", "Convertible"
        HATCHBACK = "hatchback", "Hatchback"
        TRUCK = "truck", "Truck"
        VAN = "van", "Van / Minivan"
        MOTORCYCLE = "motorcycle", "Motorcycle"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        PENDING = "pending", "Pending Sale"
        SOLD = "sold", "Sold"

    dealer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vehicles",
        limit_choices_to={"role": "dealer"},
    )

    make = models.CharField(max_length=64, db_index=True)
    model = models.CharField(max_length=64, db_index=True)
    year = models.PositiveIntegerField(db_index=True)
    trim = models.CharField(max_length=100, blank=True)
    vin = models.CharField(max_length=17, blank=True, help_text="17-character Vehicle Identification Number")

    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")

    condition = models.CharField(max_length=12, choices=Condition.choices, default=Condition.USED)
    body_style = models.CharField(max_length=16, choices=BodyStyle.choices)
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices, default=FuelType.PETROL)
    transmission = models.CharField(max_length=10, choices=Transmission.choices, default=Transmission.AUTOMATIC)
    drivetrain = models.CharField(max_length=6, choices=Drivetrain.choices, default=Drivetrain.FWD)

    mileage = models.PositiveIntegerField(default=0, help_text="In miles")
    horsepower = models.PositiveIntegerField(null=True, blank=True)
    torque_lb_ft = models.PositiveIntegerField(null=True, blank=True)
    engine = models.CharField(max_length=120, blank=True, help_text="e.g. 4.0L Twin-Turbo V8")
    exterior_color = models.CharField(max_length=64, blank=True)
    interior_color = models.CharField(max_length=64, blank=True)

    country = models.CharField(max_length=64, db_index=True)
    city = models.CharField(max_length=64, blank=True)

    description = models.TextField(blank=True)
    interior_features = models.TextField(blank=True, help_text="Comma-separated")
    exterior_features = models.TextField(blank=True, help_text="Comma-separated")
    safety_features = models.TextField(blank=True, help_text="Comma-separated")
    technology_features = models.TextField(blank=True, help_text="Comma-separated")

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    is_featured = models.BooleanField(default=False)
    is_luxury = models.BooleanField(default=False)
    is_electric_collection = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["make", "model"]),
            models.Index(fields=["price"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def get_absolute_url(self):
        return reverse("vehicles:vehicle_detail", args=[self.pk])

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img or self.images.first()


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicles/")
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "uploaded_at"]

    def __str__(self):
        return f"Image for {self.vehicle}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist_items")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "vehicle")

    def __str__(self):
        return f"{self.user} ♥ {self.vehicle}"


class SavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_searches")
    query_params = models.CharField(max_length=500, help_text="Raw querystring, e.g. make=BMW&price_max=75000")
    label = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label or self.query_params
