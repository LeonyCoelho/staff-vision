# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def update_progress(self, event):
        progress = event['progress']
        await self.send(text_data=json.dumps({'progress': progress}))
