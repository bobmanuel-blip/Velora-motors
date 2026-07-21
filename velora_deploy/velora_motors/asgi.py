import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "velora_motors.settings")

application = get_asgi_application()

# When you add real-time chat with Django Channels, this file becomes:
#
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import chatapp.routing
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(chatapp.routing.websocket_urlpatterns)
#     ),
# })
