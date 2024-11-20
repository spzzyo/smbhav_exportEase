from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginView(LoginView):
    template_name = "chat/loginPage.html"  # Specify your login template
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        # Redirect based on user_type
        if user.user_type == 1:  # Admin
            return redirect("chat-page")
        elif user.user_type == 2:  # Exporter
            return redirect("shipping-comparison")
        elif user.user_type == 3:  # Shipper
            return redirect("chat-page")
        return super().form_valid(form)
