from django.contrib import admin

from .models import SavedSearch, Vehicle, VehicleImage, Wishlist


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("__str__", "dealer", "price", "condition", "status", "country", "is_featured", "created_at")
    list_filter = ("condition", "status", "body_style", "fuel_type", "is_featured", "is_luxury", "country")
    search_fields = ("make", "model", "vin", "dealer__username")
    inlines = [VehicleImageInline]
    actions = ["mark_featured", "mark_sold"]

    @admin.action(description="Mark selected vehicles as Featured")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Mark selected vehicles as Sold")
    def mark_sold(self, request, queryset):
        queryset.update(status=Vehicle.Status.SOLD)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "vehicle", "added_at")


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "query_params", "created_at")
