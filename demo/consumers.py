import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer


class DemoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'transactionLog'

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = requests.get('https://www.uuidgenerator.net/api/version4')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message.text
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        r = requests.get('https://www.uuidgenerator.net/api/version4')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': r.text
        }))
