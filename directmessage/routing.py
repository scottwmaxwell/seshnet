from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/directmessage/<uri>/', consumers.ChatConsumer.as_asgi()),
]