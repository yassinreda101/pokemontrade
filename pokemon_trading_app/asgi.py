import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon_trading_app.settings')
django.setup()

from chat.routing import websocket_urlpatterns

print("Loading ASGI application...")
print(f"WebSocket URL patterns: {websocket_urlpatterns}")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

print("ASGI application loaded successfully!")