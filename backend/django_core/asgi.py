import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from . import urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        urls.websocket_urlpatterns
    ),
})

