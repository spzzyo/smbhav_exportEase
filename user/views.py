from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm

# views.py
class CustomLoginView(LoginView):
    template_name = "user/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 1:
            return reverse("user:admin-dashboard")
        elif user.user_type == 2:
            return reverse("user:exporter-dashboard")
        elif user.user_type == 3:
            return reverse("user:shipper-dashboard")
        elif user.user_type == 4:
            return reverse("user:actor-dashboard")
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    template_name = "user/logout.html"

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "user/register.html", {"form": form})

# @login_required
# def admin_dashboard(request):
#     return render(request, "user/admin_dashboard.html")

@login_required
def exporter_dashboard(request):
    return render(request, "user/exporter_dashboard.html")

@login_required
def shipper_dashboard(request):
    return render(request, "user/shipper_dashboard.html")

@login_required
def actor_dashboard(request):
    return render(request, "user/actor_dashboard.html")

@login_required
def shipment_tracking(request):
    return render(request, "user/shipment_tracking.html")