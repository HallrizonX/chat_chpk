from django.urls import path
from .consumers import ChatConsumer, WaitChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer),
    path('ws/chat/', WaitChatConsumer),
]
