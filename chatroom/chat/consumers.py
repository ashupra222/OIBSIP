import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type":"chat.message", "message": "new person added"})
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type":"chat.message", "message": message})

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
    
class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = None
        await self.channel_layer.group_add("vc", self.channel_name)
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        action = text_data_json['action']

        if (action == "new-offer") or (action == "new-answer"):
            receiver_channel_name = text_data_json["message"]["receiver_channel_name"]

            text_data_json["message"]["receiver_channel_name"] = self.channel_name

            await self.channel_layer.send(receiver_channel_name, {"type": "send.sdp", "recieved_dict": text_data_json})
            return

        text_data_json["message"]["receiver_channel_name"] = self.channel_name

        await self.channel_layer.group_send("vc", {"type": "send.sdp", "recieved_dict": text_data_json})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("vc", self.channel_name)
        print("disconnected")

    async def send_sdp(self, event):
        recieved_dict = event["recieved_dict"]
        if recieved_dict['message']['receiver_channel_name'] != self.channel_name:
            await self.send(text_data=json.dumps(recieved_dict))
    