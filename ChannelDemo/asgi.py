import os

from django.core.asgi import get_asgi_application
from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import ProtocolTypeRouter

from demo.consumers import DemoConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChannelDemo.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                url(r"ws/transaction-log", DemoConsumer.as_asgi()),
            ]
        )
    ),
})
