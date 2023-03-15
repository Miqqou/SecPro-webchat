import json
from channels.generic.websocket import AsyncWebsocketConsumer
 
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        "NOT IMPLEMENTED"
    
    async def disconnect(self):
        "NOT IMPLEMENTED"

    async def receive(self, text_data):
        "NOT IMPLEMENTED"
    
    async def send(self, text_data):
        "NOT IMPLEMENTED"