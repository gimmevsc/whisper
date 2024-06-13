from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .utils import send_verification_code, is_valid_email_funct, is_code_expired
import json 

from .models import User, PreRegistration
from django.db.models import Q

@csrf_exempt
def registerUser(request):
    
    if request.method == 'POST':
    
        data = json.loads(request.body.decode('utf-8'))
        
        email_address = str(data.get('email_address'))
        username = str(data.get('username'))
        password = str(data.get('password'))
        
        if username and email_address and password:
            
            if User.objects.filter(email_address=email_address).exists() or User.objects.filter(username=username).exists():
                
                if User.objects.filter(username=username).exists() and User.objects.filter(email_address=email_address).exists():
                    return JsonResponse(
                        {   
                            'message': 'Username and email address already exist',
                            'type': 'exist_username_email'
                        }, status = 400)
                
                if User.objects.filter(username=username).exists():
                    return JsonResponse(
                        {   
                            'message': 'Username already exists',
                            'type': 'exist_username'
                        }, status = 400)
                    
                if User.objects.filter(email_address=email_address).exists():
                    return JsonResponse(
                        {
                            'message': 'Email address already exists',
                            'type': 'exist_email'
                        }, status = 400)        
                
            if PreRegistration.objects.filter(Q(email_address=email_address) | Q(username=username)).exists():
                
                PreRegistration.objects.filter(Q(email_address=email_address) | Q(username=username)).delete()
                    
                    
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
    
        email = str(data.get('email_address'))
        entered_code = str(data.get('code'))
        
        pre_user = PreRegistration.objects.get(email_address = email)
        
        if pre_user.code == entered_code and not is_code_expired(pre_user.code_sent_at):    
            
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
            email = str(request.GET.get('email_address'))

            pre_user = PreRegistration.objects.get(email_address=email)
            
            new_code = send_verification_code(email)
            
            pre_user.code = str(new_code)
            pre_user.code_sent_at = timezone.now()
            pre_user.save()
            
            return JsonResponse(
                {
                    'message': 'Verification code successfully resent'
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
