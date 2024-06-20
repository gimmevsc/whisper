from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from chat.models import ChatModel
from register.models import User  # Assuming User is in register.models
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.response import Response
import jwt
from django.conf import settings
from django.http import JsonResponse


@csrf_exempt
def chatPage(request, room_name):
    
    if request.method == 'POST':
        
        try:    
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'message': 'Invalid JSON',
                    'status': 'error',
                    'type': 'invalid_json'
                }, status=400
            )
        
        receiver_id = int(room_name)
        
        sender_token = data.get('sender_token')
        
        try:
        # Decode the JWT token to get the payload
            payload = jwt.decode(sender_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']  # Assuming 'user_id' is the key in your JWT payload
            sender = get_object_or_404(User, user_id=user_id)
        except jwt.ExpiredSignatureError:
            # Handle expired token error
            raise ValueError('Token expired')
        except jwt.InvalidTokenError:
            # Handle invalid token error
            raise ValueError('Invalid token')
        except User.DoesNotExist:
            # Handle user not found error
            raise ValueError('User not found')
        
        print(sender)
        print(receiver_id)
        
        if sender.user_id < receiver_id:
            thread_name = f'{receiver_id}-{sender.user_id}'
        else:
            thread_name = f'{sender.user_id}-{receiver_id}'
        
            

        # Fetch messages from the database filtered by thread_name
        messages = ChatModel.objects.filter(thread_name=thread_name)
        
        message_list = []
        
        for message in messages:
            sender_username = message.sender
            sender_id = User.objects.get(username=sender_username)
            sender_avatar = sender.profile_picture.url if sender.profile_picture else None
            receiver = User.objects.get(user_id=receiver_id)
            receiver_avatar = receiver.profile_picture.url if receiver.profile_picture else None
            
            message_list.append({
                'sender': sender_id.user_id,
                'sender_avatar': sender_avatar,
                'receiver_avatar': receiver_avatar,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse(
                {
                    'message': message_list
                }, status=200
            )
        
    return Response({'error': 'Invalid request method'}, status=400)
        # print(sender)
        # Retrieve chat messages between sender and receiver
        # messages = ChatMessage.objects.filter(sender=sender, receiver_id=receiver_id).order_by('timestamp')
        # serializer = ChatMessageSerializer(messages, many=True)

        # # Retrieve sender's and receiver's profile pictures (if available)
        # sender_profile = get_object_or_404(UserProfile, user=sender)
        # receiver = get_object_or_404(User, id=receiver_id)
        # receiver_profile = get_object_or_404(UserProfile, user=receiver)

        # # Serialize profile picture URLs (or base64 encoded images) if needed
        # sender_avatar_url = sender_profile.profile_picture.url if sender_profile.profile_picture else None
        # receiver_avatar_url = receiver_profile.profile_picture.url if receiver_profile.profile_picture else None

        # return Response({
        #     'messages': serializer.data,
        #     'sender_avatar_url': sender_avatar_url,
        #     'receiver_avatar_url': receiver_avatar_url
        # })