from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("chat/<other_user_id>", consumers.ChatConsumer.as_asgi()),
]