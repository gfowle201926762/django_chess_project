from django.urls import path
from .views import Home, ChessRoom

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('game/<str:chess_room_name>/', ChessRoom.as_view(), name='chess_room'),
] 