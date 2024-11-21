
from channels.routing import ProtocolTypeRouter, URLRouter
from chatPortal import routing
from channels.auth import AuthMiddlewareStack

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatPortal import routing as chatPortal_routing  # Existing routing from ChitChat
from notification.routing import websocket_urlpatterns as notification_routing  # Import notification routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exportEase.settings')

# Combine WebSocket routing from multiple apps
combined_websocket_urlpatterns = chatPortal_routing.websocket_urlpatterns + notification_routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                combined_websocket_urlpatterns  # Use combined WebSocket routing
            )
        ),
    }
)
