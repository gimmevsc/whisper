import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from chat.models import ChatModel
from register.models import User  # Assuming User is in register.models
from base64 import b64encode

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
            return JsonResponse(
                {
                    'message': 'Token expired',
                    'status': 'error',
                    'type': 'token_expired'
                }, status=401
            )
        except jwt.InvalidTokenError:
            # Handle invalid token error
            return JsonResponse(
                {
                    'message': 'Invalid token',
                    'status': 'error',
                    'type': 'invalid_token'
                }, status=401
            )
        except User.DoesNotExist:
            # Handle user not found error
            return JsonResponse(
                {
                    'message': 'User not found',
                    'status': 'error',
                    'type': 'user_not_found'
                }, status=404
            )
        
        if sender.user_id < receiver_id:
            thread_name = f'{receiver_id}-{sender.user_id}'
        else:
            thread_name = f'{sender.user_id}-{receiver_id}'

        # Fetch messages from the database filtered by thread_name
        messages = ChatModel.objects.filter(thread_name=thread_name)
        
        receiver = get_object_or_404(User, user_id=receiver_id)
        
        sender_req = sender.user_id

        def get_avatar_base64(user):
            if user.profile_picture:
                with open(user.profile_picture.path, "rb") as image_file:
                    return b64encode(image_file.read()).decode('utf-8')
            return None

        receiver_avatar = get_avatar_base64(receiver)
        sender_avatar = get_avatar_base64(sender)
        
        message_list = []
        
        for message in messages:
            sender_username = message.sender
            sender_id = get_object_or_404(User, username=sender_username)
            message_list.append({
                'sender': sender_id.user_id,
                'username': sender_username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse(
            {
                'message': message_list,
                'sender_id': sender_req,
                'sender_username' : sender.username,
                'receiver_avatar': receiver_avatar,
                'sender_avatar': sender_avatar,
                'receiver_username' : receiver.username
            }, status=200
        )
        
    return JsonResponse(
        {
            'error': 'Invalid request method'
        }, status=400
    )
