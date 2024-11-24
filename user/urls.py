from django.urls import path, include
from .views import *
from doc_manager.views import actor_Dashboard_with_all_docs, admin_dashboard, process_forgery_checks



app_name = "user"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    path("exporter-dashboard/", exporter_dashboard, name="exporter-dashboard"),
    path("shipper-dashboard/", shipper_dashboard, name="shipper-dashboard"),
    path("actor-dashboard/", actor_Dashboard_with_all_docs, name="actor-dashboard"),
    path("process_forgery_checks/", process_forgery_checks, name="process_forgery_checks"),
    
]