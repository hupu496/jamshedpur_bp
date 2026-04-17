from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MonitorConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(json.dumps({
            "type": "connected",
            "message": "WebSocket connected"
        }))

    async def disconnect(self, close_code):
        print("Client disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get("type") == "heartbeat":
            await self.send(json.dumps({
                "type": "heartbeat",
                "status": "alive"
            }))
