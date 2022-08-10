import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random



class Counter():
    def __init__(self):
        self.rooms = {}

    def append_if_absent(self, group_name):
        present = False
        for room_name in self.rooms:
            if group_name == room_name:
                present = True
        if present == False:
            self.rooms[group_name] = 0

    def increment_and_check_room_size(self, group_name):
        if self.rooms[group_name] + 1 > 2:
            return False
        
        if self.rooms[group_name] + 1 <= 2:
            self.rooms[group_name] += 1
            return True

    def decrement_and_check_room_deletion(self, group_name):
        if self.rooms[group_name] - 1 > 0:
            self.rooms[group_name] -= 1

        if self.rooms[group_name] - 1 == 0:
            self.rooms.pop(group_name)

counter = Counter()


class ChessRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chess_room_name = self.scope['url_route']['kwargs']['chess_room_name']
        self.group_name = 'game_%s' % self.chess_room_name

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        counter.append_if_absent(self.group_name)
        allowed = counter.increment_and_check_room_size(self.group_name)

        if allowed == True:
            await self.accept()

        if allowed == False:
            print("CONNECTION REJECTED")
            return

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'] # assuming the message is keyed to 'message'
        type = text_data_json['type']
        

        if type == 'move':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'play_move',
                    'sender': self.channel_name,
                    'message': message
                }
            )

        if type == 'start':
            
            x = random.randint(0, 1)
            if x == 0:
                message = 'white'

            if x == 1:
                message = 'black'
            
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'start_game', 
                    'sender': self.channel_name,
                    'message': message
                }
            ) 



    async def start_game(self, text_data):
        message = text_data['message']
        please = text_data['sender']

        if please != self.channel_name:
            if message == 'white':
                message = 'black'
            elif message == 'black':
                message = 'white'

        await self.send(text_data=json.dumps({
                'type': 'start_game',
                'message': message
            }))
                




    async def play_move(self, text_data):
        message = text_data['message']
        sender = text_data['sender']

        if sender != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'play_move',
                'message': message
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        counter.decrement_and_check_room_deletion(self.group_name)
