import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from .models import ChatModel, ChatGroup, GroupMessage
from chat.tokenauthentication import JWTAuthentication
from asgiref.sync import sync_to_async  # Import sync_to_async

User = get_user_model()

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the JWT token from cookies
        token = self.scope['cookies'].get('token')
        if not token:
            await self.close(code=4001)
            return
        
        # Decode the JWT token to get the user information
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            self.scope['user'] = await sync_to_async(User.objects.get)(user_id=user_id)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist) as e:
            await self.close(code=4001)
            return
        
        # Get the other user ID from the URL route
        other_user_id = self.scope['url_route']['kwargs']['user_id']
        # user = self.scope['user']
        # Determine the room name based on user IDs
        my_id = self.scope['user'].user_id
        
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'
        
        self.room_group_name = f'chat_{self.room_name}'
        # Add the channel to the group
        # print(self.room_group_name, user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        # data = json.loads(text_data)
        # message = data['message']
        message = text_data
        # Save the message to the database
        await self.save_message(message)
        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope['user'].username
            }
        )


    async def save_message(self, message):
        # Save the message to the database
        await sync_to_async(ChatModel.objects.create)(
            sender=self.scope['user'].username,
            message=message,
            thread_name=self.room_name
        )

    
    async def chat_message(self, event):
        print(event)
        message = event['message']
        username = event['username']
        print(message, username)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sdfs' : 'sdfs'
        }))
        
    
# class GroupChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Extract the JWT token from cookies
#         token = self.scope['cookies'].get('token')
#         if not token:
#             await self.close(code=4001)
#             return
        
#         # Decode the JWT token to get the user information
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = payload['user_id']
#             self.scope['user'] = await sync_to_async(User.objects.get)(id=user_id)
#         except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
#             await self.close(code=4001)
#             return
        
#         # Get the group name from the URL route
#         self.group_name = self.scope['url_route']['kwargs']['group_name']
#         self.room_group_name = f'group_{self.group_name}'
        
#         # Add the channel to the group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
        
#         # Save the message to the database
#         await self.save_message(message)
        
#         # Send the message to the group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'group_message',
#                 'message': message,
#                 'username': self.scope['user'].username
#             }
#         )

#     async def save_message(self, message):
#         # Save the message to the database
#         group = await sync_to_async(ChatGroup.objects.get)(group_name=self.group_name)
#         await sync_to_async(GroupMessage.objects.create)(
#             group=group,
#             author=self.scope['user'],
#             body=message
#         )

#     async def group_message(self, event):
#         message = event['message']
#         username = event['username']
        
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username
#         }))