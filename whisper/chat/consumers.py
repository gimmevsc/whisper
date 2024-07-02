import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from .models import *
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
        other_user_id = int(self.scope['url_route']['kwargs']['user_id'])
        # user = self.scope['user']
        # Determine the room name based on user IDs
        my_id = int(self.scope['user'].user_id)        
        
        self.room_group_name = f'{min(my_id, other_user_id)}-{max(my_id, other_user_id)}'
        title = self.room_group_name
        
        if other_user_id == my_id:
            chat_type = 'saved_messages'
        else:
            chat_type = 'personal'
                        
        # Get or create the chat based on type and title
        try:
            chat = await sync_to_async(Chat.objects.get)(chat_type=chat_type, title=title)
        except Chat.DoesNotExist:
            chat = await sync_to_async(Chat.objects.create)(chat_type=chat_type, title=title)
        
        # Create participants for the chat
        my_participant, created_my_participant = await sync_to_async(Participant.objects.get_or_create)(user_id=my_id, chat=chat)
        other_participant, created_other_participant = await sync_to_async(Participant.objects.get_or_create)(user_id=other_user_id, chat=chat)
        
        
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
        # print(text_data)
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
                'username': self.scope['user'].username,
                'sender_id' : self.scope['user'].user_id
            }
        )


    async def save_message(self, message):
        chat = await sync_to_async(Chat.objects.get)(title=self.room_group_name)
        await sync_to_async(Message.objects.create)(
            chat=chat,
            sender=self.scope['user'],
            message_content=message
        )

    
    async def chat_message(self, event):
        print(event)
        message = event['message']
        username = event['username']
        sender_id = event['sender_id']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sender' : sender_id
            
        }))
        

# class OnlineStatusConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = 'user'
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         username = data['username']
#         connection_type = data['type']
#         print(connection_type)
#         await self.change_online_status(username, connection_type)

#     async def send_onlineStatus(self, event):
#         data = json.loads(event.get('value'))
#         username = data['username']
#         online_status = data['status']
#         await self.send(text_data=json.dumps({
#             'username':username,
#             'online_status':online_status
#         }))


#     async def disconnect(self, message):
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     @database_sync_to_async
#     def change_online_status(self, username, c_type):
#         user = User.objects.get(username=username)
#         userprofile = UserProfileModel.objects.get(user=user)
#         if c_type == 'open':
#             userprofile.online_status = True
#             userprofile.save()
#         else:
#             userprofile.online_status = False
#             userprofile.save()


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