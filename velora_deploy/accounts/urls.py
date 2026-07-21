from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dealer/dashboard/", views.dealer_dashboard, name="dealer_dashboard"),
    path("buyer/dashboard/", views.buyer_dashboard, name="buyer_dashboard"),
]
