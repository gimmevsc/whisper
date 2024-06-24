import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from chat.models import Chat, Message, Participant
from register.models import User
from django.core.exceptions import ObjectDoesNotExist
from .utils import get_avatar_base64, get_users_with_shared_chats

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

        # token = data.get('sender_token')

        user_id = str(data.get('user_id'))
        
        try:
            # Decode the JWT token to get the payload
            # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # user_id = payload['user_id']  # Assuming 'user_id' is the key in your JWT payload
            sender = get_object_or_404(User, user_id=user_id)
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

        if sender.user_id == receiver_id:
            chat_type = 'saved_messages'
        else:
            chat_type = 'personal'
        # Get or create the chat
        chat = Chat.objects.get(chat_type=chat_type, title=thread_name)
        # Fetch or create participants
        # my_participant, created_my_participant = Participant.objects.get_or_create(user_id=sender.user_id, chat=chat)
        # other_participant, created_other_participant = Participant.objects.get_or_create(user_id=receiver_id, chat=chat)
        # Fetch messages from the database filtered by chat
        messages = Message.objects.filter(chat=chat).order_by('sent_at')

        receiver = get_object_or_404(User, user_id=receiver_id)

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


def userSearch(request):
    if request.method == 'GET':
        try:
            username_contains = request.GET.get('username')
            
            if not username_contains:
                return JsonResponse(
                    {
                        'message': 'Please provide a search term'
                    }, status=400)
            
            # Perform case-insensitive 'contains' search on username field
            users = User.objects.filter(username__icontains=username_contains)
            
            if not users.exists():
                return JsonResponse(
                    {
                        'message': 'No users found matching the search term'
                    }, status=404)
            
            users_list = []

            for user in users:
                users_list.append({
                    'user_id': user.user_id,
                    'username': user.username,
                    'profile_picture': get_avatar_base64(user)
                })
            
            return JsonResponse(users_list, safe=False, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    'message': 'User not found'
                }, status=200)
        
        except Exception as e:
            return JsonResponse(
                {
                    'message': str(e)
                }, status=500)
    
    else:
        return JsonResponse(
            {
                'message': 'Method not allowed'
            }, status=405)



def userChats(request):
    
    if request.method == 'GET':
        
        try:
            user_id = str(request.GET.get('user_id'))
            
            base_user = get_object_or_404(User, user_id=user_id)
            
            users_with_shared_chats = get_users_with_shared_chats(base_user)
            
            chat = Chat.objects.get(chat_type='saved_messages', title=f'{user_id}-{user_id}')

            user_list = []

            for user in users_with_shared_chats:
                user_list.append({
                'user_id': user.user_id,
                'username': user.username,
                'profile_picture' : get_avatar_base64(user)
            })  
                
            return JsonResponse({
                'saved_messages_chat_id' : chat.chat_id,
                'user_list' : user_list 
                }, status=200)
        
        except ObjectDoesNotExist:
        
            return JsonResponse(
                {
                    'message': 'User not found'
                }, status=404)
        
        except Exception as e:
        
            return JsonResponse(
                {
                    'message': str(e)
                }, status=500)
    else:
        
        return JsonResponse(
            {
                'message': 'Method not allowed'
            }, status=405)