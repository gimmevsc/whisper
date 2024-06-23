import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from chat.models import Chat, Message, Participant
from register.models import User
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

        token = data.get('sender_token')

        try:
            # Decode the JWT token to get the payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
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

        receiver_id = int(room_name)

        # Determine the thread name based on user IDs
        thread_name = f'{min(sender.user_id, receiver_id)}-{max(sender.user_id, receiver_id)}'

        # Get or create the chat
        chat, created = Chat.objects.get_or_create(chat_type='personal', title=thread_name)

        # Fetch or create participants
        # my_participant, created_my_participant = Participant.objects.get_or_create(user_id=sender.user_id, chat=chat)
        # other_participant, created_other_participant = Participant.objects.get_or_create(user_id=receiver_id, chat=chat)

        # Fetch messages from the database filtered by chat
        messages = Message.objects.filter(chat=chat).order_by('sent_at')

        receiver = get_object_or_404(User, user_id=receiver_id)

        def get_avatar_base64(user):
            if user.profile_picture:
                with open(user.profile_picture.path, "rb") as image_file:
                    return b64encode(image_file.read()).decode('utf-8')
            return None

        receiver_avatar = get_avatar_base64(receiver)
        sender_avatar = get_avatar_base64(sender)

        message_list = []

        for message in messages:
            message_list.append({
                'sender': message.sender_id,
                'username': message.sender.username,
                'message': message.message_content,
                'timestamp': message.sent_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse(
            {
                'message': message_list,
                'sender_id': sender.user_id,
                'sender_username': sender.username,
                'receiver_avatar': receiver_avatar,
                'sender_avatar': sender_avatar,
                'receiver_username': receiver.username
            }, status=200
        )

    return JsonResponse(
        {
            'error': 'Invalid request method'
        }, status=400
    )
