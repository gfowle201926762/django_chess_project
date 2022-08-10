from django.urls import path, re_path
from .consumers import ChessRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chess_room/(?P<chess_room_name>\w+)/$', ChessRoomConsumer.as_asgi())
]