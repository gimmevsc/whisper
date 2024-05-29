from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .utils import send_verification_code, is_valid_email_funct, is_code_expired
import json 

from .models import User
from .models import PreRegistration

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
            
            if PreRegistration.objects.filter(email_address=email_address).exists():
                
                try:
                    user_to_delete = PreRegistration.objects.get(email_address=email_address)
                    user_to_delete.delete()
            
                except PreRegistration.DoesNotExist:
                    print("User does not exist.")
                
            if PreRegistration.objects.filter(username=username).exists():
                
                try:
                    user_to_delete = PreRegistration.objects.get(username=username)
                    user_to_delete.delete()
            
                except PreRegistration.DoesNotExist:
                    print("User does not exist.")
                    
            if not is_valid_email_funct(email_address):
                return JsonResponse(
                    { 
                        'message': 'Invalid email address',
                        'type': 'invalid_email'
                    }, status = 400)              
            
            code = send_verification_code(email_address)
            
            user = PreRegistration.objects.create(username=username, email_address=email_address, password=password, 
                                       code=code, code_sent_at=timezone.now())
                        
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
        
        # pre_user = PreRegistration.objects.get(email_address = 'bodya190505@gmail.com')
        
        pre_user = PreRegistration.objects.get(email_address = email)
        
        if pre_user.code == entered_code and not is_code_expired(pre_user.code_sent_at):    
            
            print('sdfsdfsdfsdfsdfsdf')
            user = User.objects.create(username=pre_user.username, email_address=pre_user.email_address, password=pre_user.password)
            user.save()
            
            pre_user.delete()
            
            return JsonResponse(
                {
                    'status': 'success'
                }, status = 200) 
            
        elif pre_user.code != entered_code:
            return JsonResponse(
                {          
                    'type': 'wrong code'
                }, status = 400)
        else:
            return JsonResponse(
                {          
                    'type': 'code expired'
                }, status = 400)
            
    else:
        return JsonResponse(
                {
                    'message': 'Bad request',
                    'type': 'bad_request'
                }, status = 405)    


@csrf_exempt
def resendConfirmationCode(request):
    
    if request.method == 'GET':
        
        try:
            
            email = request.GET.get('email_address')
    
            user = User.objects.get(email_address=email)
            
            new_code = send_verification_code(email)
            
            user.code = new_code
            user.code_sent_at = timezone.now()
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
