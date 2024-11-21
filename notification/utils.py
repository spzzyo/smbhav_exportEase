from .models import Notification

def send_notification(sender, recipient, message):
    Notification.objects.create(sender=sender, recipient=recipient, message=message)
    # Send real-time notification via WebSocket
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",
        {"type": "send_notification", "message": message},
    )
