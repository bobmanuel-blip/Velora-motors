from django.urls import path

from . import views

app_name = "vehicles"

urlpatterns = [
    path("", views.vehicle_list, name="vehicle_list"),
    path("compare/", views.compare_vehicles, name="compare"),
    path("new/", views.dealer_vehicle_create, name="vehicle_create"),
    path("<int:pk>/", views.vehicle_detail, name="vehicle_detail"),
    path("<int:pk>/edit/", views.dealer_vehicle_update, name="vehicle_update"),
    path("<int:pk>/delete/", views.dealer_vehicle_delete, name="vehicle_delete"),
    path("<int:pk>/wishlist/", views.wishlist_toggle, name="wishlist_toggle"),
]
