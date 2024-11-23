from django.db import models
from user.models import CustomUser

class Notification(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_notifications")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.sender} to {self.recipient}: {self.message}"
