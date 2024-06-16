from django.http import JsonResponse
from register.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
from django.contrib.auth import authenticate
from django.conf import settings
import jwt

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            username_or_email = data.get('username')
            password = data.get('password')

            try:
                # Try to validate the email
                validate_email(username_or_email)
                # If the email is valid, fetch the user by email
                user = User.objects.get(email_address=username_or_email)
                username = user.username
            except ValidationError:
                # If validation error occurs, treat it as a username
                username = username_or_email
                user = authenticate(username = username, password=password)
                
                if not user:
                    return JsonResponse(
                        {
                            'message': 'Username does not exist'
                        }, status=400)
                    
            except User.DoesNotExist:
                return JsonResponse(
                    {
                        'message': 'Email address does not exist'
                    }, status=400)

            # Check if the password is correct
            user = authenticate(username=username, password=password)
            
            if user is not None:
                payload = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email_address' : user.email_address,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name            
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                return JsonResponse(
                    {
                        'message': 'Login successful',
                        'token': token
                    }, status=200)
            else:
                return JsonResponse(
                    {
                        'message': 'Invalid password'
                    }, status=400)

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'message': 'Invalid JSON data in request body'
                }, status=400)
        except Exception as e:
            return JsonResponse(
                {
                    'message': 'An error occurred'
                }, status=500)
    else:
        return JsonResponse(
            {
                'message': 'Only POST requests are allowed'
            }, status=405)