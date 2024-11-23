from django.contrib.auth.decorators import login_required
from .models import Notification
from user.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import send_notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")
    return render(request, "notification/notification_list.html", {"notifications": notifications})



def send_custom_notification(request):
    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        message = request.POST.get("message")
        try:
            recipient = CustomUser.objects.get(id=recipient_id)
            if request.user.is_authenticated and request.user != recipient:
                send_notification(request.user, recipient, message)
                messages.success(request, f"Notification sent to {recipient.username}!")
            else:
                messages.error(request, "You cannot send notifications to yourself or without logging in.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Recipient not found.")
        return redirect("send_notification")

    # Provide a list of users (excluding admin if necessary) for sending notifications
    users = CustomUser.objects.exclude(id=request.user.id)  # Exclude the logged-in user
    if not request.user.is_staff:
        users = users.filter(is_staff=False)  # Exclude staff for non-admin users

    return render(request, "notification/send_notification.html", {"users": users})
