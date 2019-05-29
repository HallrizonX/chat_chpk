import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

from .database.query import get_old_messages, write_message_to_db, create_new_room, get_counts_unread_messages
from .database.message import messages_response, format_message, valid_message


class WaitChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username: str = self.scope['user'] if self.scope['user'] else 'Anon'

        self.user: str = f'{self.username}'
        self.room_group_name: str = f'user_{self.user}'

        # Join room group
        await self.channel_layer.group_add(
            self.user,
            self.channel_name
        )

        await get_counts_unread_messages(self.username)

        await self.accept()
        while True:
            await asyncio.sleep(3)
            await self.send(text_data=json.dumps(await get_counts_unread_messages(self.username)))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.user,
            self.channel_name
        )


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.username: str = self.scope['user'] if self.scope['user'] else 'Anon'
        self.room_name: str = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name: str = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if not await create_new_room(self.room_name):
            room, messages = await get_old_messages(self.username, self.room_name)
            if messages and room:
                # Send message to WebSocket
                await self.send(text_data=json.dumps({
                    'message': await messages_response(messages)
                }))

    # Receive message from room group and send to client
    async def chat_message(self, event):
        message = event['message']

        await get_old_messages(self.username, self.room_name)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message: str = text_data_json['message']

        if await valid_message(message):
            if await write_message_to_db(self.room_name, self.username, message):
                message = await format_message(self.username, message)
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
