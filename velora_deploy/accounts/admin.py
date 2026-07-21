from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import DealerProfile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_dealer_display", "is_active", "created_at")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Velora Motors Profile", {"fields": ("role", "phone_number", "country", "avatar", "two_factor_enabled")}),
    )

    @admin.display(boolean=True, description="Dealer")
    def is_dealer_display(self, obj):
        return obj.is_dealer


@admin.register(DealerProfile)
class DealerProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "city", "country", "is_verified", "quality_score")
    list_filter = ("is_verified", "country")
    search_fields = ("company_name", "user__username", "user__email")
    actions = ["verify_dealers"]

    @admin.action(description="Mark selected dealers as Verified")
    def verify_dealers(self, request, queryset):
        queryset.update(is_verified=True)
