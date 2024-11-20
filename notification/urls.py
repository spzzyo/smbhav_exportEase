from django.urls import path
from .views import notification_list, send_custom_notification

urlpatterns = [
    path("", notification_list, name="notification-list"),
    path("send/", send_custom_notification, name="send_notification"),
]
