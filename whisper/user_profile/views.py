import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from chat.models import ChatModel
from register.models import User 
from base64 import b64encode

# Create your views here.
@csrf_exempt
def setUpProfile(request):
    
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
        