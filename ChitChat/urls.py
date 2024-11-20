from django.urls import path, include
from ChitChat import views as chat_views
from .views import comparison
from django.contrib.auth.views import LoginView, LogoutView
from user import views as user_views

urlpatterns = [
    # authentication section
    path("auth/login/", user_views.CustomLoginView.as_view(template_name="chat/loginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path("carriers", comparison, name="shipping-comparison" ),
    path("chat", chat_views.chatPage, name="chat-page"),
]