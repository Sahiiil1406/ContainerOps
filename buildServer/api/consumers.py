import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RunConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'run_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def run_data(self, event):
        # Send data to WebSocket
        await self.send(text_data=json.dumps(event['data']))