from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extends Django's built-in user with the roles Velora Motors needs."""

    class Role(models.TextChoices):
        BUYER = "buyer", "Buyer"
        DEALER = "dealer", "Dealer"
        ADMIN = "admin", "Platform Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)
    phone_number = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_dealer(self):
        return self.role == self.Role.DEALER

    @property
    def is_buyer(self):
        return self.role == self.Role.BUYER

    def __str__(self):
        return self.get_full_name() or self.username


class DealerProfile(models.Model):
    """Extra business info attached to a User with role=dealer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dealer_profile")
    company_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="dealer_logos/", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False, help_text="Verified Dealer badge")
    quality_score = models.DecimalField(
        max_digits=4, decimal_places=2, default=0,
        help_text="AI-computed dealer quality score (0-100), placeholder for now",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dealer Profile"
        verbose_name_plural = "Dealer Profiles"

    def __str__(self):
        return self.company_name
