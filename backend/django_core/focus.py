from channels.generic.websocket import AsyncWebsocketConsumer
import json

class Focus(AsyncWebsocketConsumer):
    connected_clients = set()

    async def connect(self):
        await self.accept()
        self.connected_clients.add(self)

    async def disconnect(self, close_code):
        self.connected_clients.remove(self)

    async def receive(self, text_data):
        for client in self.connected_clients:
            if client != self:
                await client.send(json.dumps({
                    'locknum': text_data
                }))
