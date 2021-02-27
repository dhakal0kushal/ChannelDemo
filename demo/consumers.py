import json
import requests
import channels
from channels.generic.websocket import AsyncWebsocketConsumer
from demo.models import Demo
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync



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
    async def send_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': "id:" + str(event['data']['id'])+ ", text:" + event['data']['text'] + ", number:" + str(event['data']['number'])
        }))

    @receiver(post_save, sender=Demo)
    def order_offer_observer(sender, instance, **kwargs):
        layer = channels.layers.get_channel_layer()

        async_to_sync(layer.group_send)('transactionLog', {
            'type': 'send_message',
            'data': {
                'text': instance.text,
                'number': instance.number,
                'id': instance.pk
            }
        })
