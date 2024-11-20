from django.urls import path, include
from ChitChat import views as chat_views
from .views import comparison

urlpatterns = [
    path("carriers", comparison, name="shipping-comparison" ),
    path("chat", chat_views.chatPage, name="chat-page"),
]