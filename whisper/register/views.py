from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from re import match
from .utils import send_verification_code
import json 

from .models import User

def is_valid_email(email):
    regex = r'^.+@.+$'
    if match(regex, email):
        return True
    return False


@csrf_exempt
def registerUser(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
        
        email_address = data.get('email_address')
        username = data.get('username')
        password = data.get('password')
        
        
        if username and email_address and password:
            
            if User.objects.filter(email_address=email_address).exists():
                return JsonResponse(
                    {
                        'message': 'Email address already exists',
                        'type': 'exist_email'
                    }, status = 400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {   
                        'message': 'Username already exists',
                        'type': 'exist_username'
                    }, status = 400)
             
            if not is_valid_email(email_address):
                return JsonResponse(
                    { 
                        'message': 'Invalid email address',
                        'type': 'invalid_email'
                    }, status = 400)
            
            code = send_verification_code(email_address)
            
            user = User.objects.create(username=username, email_address=email_address, password=password, code=code, is_valid = False)
                        
            user.save()
            
            return JsonResponse(
                {   
                    'message': 'success'
                }, status = 200)
        else:
            return JsonResponse(
                {
                    'message': 'Empty field',
                    'type': 'empty_email'
                },status = 400)

    else:
        return JsonResponse(
                {
                    'message': 'Bad request',
                    'type': 'bad_request'
                }, status = 405)


@csrf_exempt
def emailConfirmation(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
    
        email = data.get('email_address')
        entered_code = data.get('code')
        
        user = User.objects.get(email_address = email)        
        
        if user.code == entered_code:    
            
            user.is_valid = True
            
            return JsonResponse(
                {
                    'status': 'success'
                }, status = 200) 
        else:
            return JsonResponse(
                {          
                    'type': 'wrong code'
                }, status = 400)
    else:
        return JsonResponse(
                {
                    'message': 'Bad request',
                    'type': 'bad_request'
                }, status = 405)    


@csrf_exempt
def resendCode(request):
    
    if request.method == 'GET':
        
        try:
            
            email = request.GET.get('email_address')
    
            user = User.objects.get(email_address=email)
            
            new_code = send_verification_code(email)
            
            user.code = new_code

            user.save()
            
            return JsonResponse(
                {
                    'message': 'Verification code resent successfully'
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
