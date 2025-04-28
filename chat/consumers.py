import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Print debug information
        print(f"WebSocket connect attempt. Path: {self.scope['path']}")
        print(f"URL route: {self.scope.get('url_route', {})}")

        # Extract room name from path if not in kwargs
        if 'url_route' not in self.scope or 'kwargs' not in self.scope['url_route'] or 'room_name' not in self.scope['url_route']['kwargs']:
            path = self.scope['path']
            parts = path.split('/')
            # Find the part after 'chat'
            try:
                chat_index = parts.index('chat')
                if chat_index + 1 < len(parts):
                    self.room_name = parts[chat_index + 1]
                else:
                    self.room_name = 'default'
            except ValueError:
                # If 'chat' not found, use the second-to-last part if available
                self.room_name = parts[-2] if len(parts) >= 2 else 'default'

            print(f"Room name extracted from path: {self.room_name}")
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            print(f"Room name from kwargs: {self.room_name}")

        self.room_group_name = f'chat_{self.room_name}'
        print(f"Room group name: {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"WebSocket connection accepted for room: {self.room_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Save message to database
        timestamp = await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': timestamp.isoformat() if timestamp else timezone.now().isoformat()
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        try:
            # Get room and sender
            from accounts.models import Trainer
            from django.shortcuts import get_object_or_404

            room = get_object_or_404(ChatRoom, name=self.room_name)
            sender = get_object_or_404(Trainer, username=username)

            # Create and save message
            chat_message = ChatMessage.objects.create(
                room=room,
                sender=sender,
                content=message
            )

            return chat_message.timestamp
        except Exception as e:
            print(f"Error saving message: {e}")
            return None