from django.shortcuts import render
from django.views import View

# Create your views here.


class Home(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'main/home.html', context)

class ChessRoom(View):
    def get(self, request, chess_room_name, *args, **kwargs):
        context = {
            'chess_room_name': chess_room_name
        }
        return render(request, 'main/chess_room.html', context)