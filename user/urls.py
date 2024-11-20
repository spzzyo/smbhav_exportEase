from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    path("exporter-dashboard/", exporter_dashboard, name="exporter-dashboard"),
    path("shipper-dashboard/", shipper_dashboard, name="shipper-dashboard"),
]