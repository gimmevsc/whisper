import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from register.models import User 
from base64 import b64decode
from chat.tokenauthentication import JWTAuthentication
from django.core.files.base import ContentFile

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
        
        token = data.get('token')
        print(data)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = get_object_or_404(User, user_id=user_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {
                    'message': 'Token expired',
                    'status': 'error',
                    'type': 'token_expired'
                }, status=401
            )
        except jwt.InvalidTokenError:
            return JsonResponse(
                {
                    'message': 'Invalid token',
                    'status': 'error',
                    'type': 'invalid_token'
                }, status=401
            )
        except User.DoesNotExist:
            return JsonResponse(
                {
                    'message': 'User not found',
                    'status': 'error',
                    'type': 'user_not_found'
                }, status=404
            )
        
        new_username = data.get('username')
        new_email = data.get('email_address')
        new_phone_number = data.get('phone_number')
        new_first_name = data.get('first_name')
        new_last_name = data.get('last_name')
        new_bio = data.get('bio')
        profile_picture_base64 = data.get('profile_picture')
        print(profile_picture_base64)

        # Check for unique constraints
        if new_username and User.objects.filter(username=new_username).exclude(user_id=user_id).exists():
            return JsonResponse(
                {
                    'message': 'Username already exists',
                    'status': 'error',
                    'type': 'username_exists'
                }, status=400
            )

        if new_email and User.objects.filter(email_address=new_email).exclude(user_id=user_id).exists():
            return JsonResponse(
                {
                    'message': 'Email address already exists',
                    'status': 'error',
                    'type': 'email_exists'
                }, status=400
            )

        if new_phone_number and User.objects.filter(phone_number=new_phone_number).exclude(user_id=user_id).exists():
            return JsonResponse(
                {
                    'message': 'Phone number already exists',
                    'status': 'error',
                    'type': 'phone_exists'
                }, status=400
            )
        print(new_last_name)
        # Update user profile
        if new_username:
            user.username = new_username
        if new_email:
            user.email_address = new_email
        if new_phone_number:
            user.phone_number = new_phone_number
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name
        if new_bio:
            user.bio = new_bio

        # Handle profile picture update
        if profile_picture_base64:
            format, imgstr = profile_picture_base64.split(';base64,') 
            ext = format.split('/')[-1] 
            profile_picture_data = ContentFile(b64decode(imgstr), name=f'{user.username}.{ext}')
            user.profile_picture = profile_picture_data

        user.save()

        # Generate a new token with updated information
        updated_payload = {
            'user_id': user.user_id,
            'username': user.username,
            'email_address': user.email_address,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'phone_number': user.phone_number,
            # 'profile_picture': user.profile_picture.url if user.profile_picture else None
        }

        new_token = JWTAuthentication.generate_token(updated_payload)
    
        return JsonResponse(
            {
                'message': 'Profile updated successfully',
                'token': new_token
            }, status=200)
    
    return JsonResponse(
        {
            'error': 'Invalid request method'
        }, status=400)
