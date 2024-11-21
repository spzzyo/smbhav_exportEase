import json
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = self.scope['query_string'].decode()  # Get the raw query string
        params = dict(param.split('=') for param in query_params.split('&'))  

        username = params.get("username")
        carrier_name = params.get("carrier_name")

  
        self.roomGroupName = f"{username}_{carrier_name}"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        time = text_data_json["time"]
        roomId = self.roomGroupName

        await self.save_message(username, message,roomId)

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "time": time
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        time = event["time"]
        

        await self.send(text_data=json.dumps({"message": message, "username": username, "time": time}))




    @sync_to_async
    def save_message(self, username, message,roomId):
        #

        # Save to the database
        return Messages.objects.create(username=username, message=message, roomId = roomId)