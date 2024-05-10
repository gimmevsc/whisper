from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from re import match
import json 

from .models import User

def is_valid_email(email):
    regex = r'^.+@.+$'
    if match(regex, email):
        return True
    return False


@csrf_exempt
def registerUser(request):
    
    print(request.body)
    
    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
        
        email_address = data.get('email_address')
        username = data.get('username')
        password = data.get('password')
        
        print(email_address)
        
        if username and email_address and password:
            
            if User.objects.filter(email_address=email_address).exists():
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Email address already exists',
                        'type': 'exist_email'
                    })
            
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {   'status': 'error',
                        'message': 'Username already exists',
                        'type': 'exist_username'
                    })
             
            if not is_valid_email(email_address):
                return JsonResponse(
                    {   'status': 'error',
                        'message': 'Invalid email address',
                        'type': 'invalid_email'
                    })
            
            user = User.objects.create(username=username, email_address=email_address, password=password)
            
            user.save()

            return JsonResponse(
                {   
                    'status': 'success'
                })
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Empty field',
                    'type': 'empty_email'
                })

    else:
        return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Bad request',
                    'type': 'bad_request'
                })
