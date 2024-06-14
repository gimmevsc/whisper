from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
from django.utils import timezone
from register.models import User, PreRegistration
from reset_password.models import PasswordReset
from django.http import JsonResponse
from register.utils import send_verification_code, is_code_expired

@csrf_exempt
def enterEmail(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'message': 'Invalid JSON',
                    'type': 'invalid_json'
                }, status=400
            )

        email_address = data.get('email_address')

        if not email_address:
            return JsonResponse(
                {
                    'message': 'Email field is empty',
                    'type': 'empty_email'
                }, status=400
            )

        try:
            validate_email(email_address)
        except ValidationError:
            return JsonResponse(
                {
                    'message': 'Invalid email format',
                    'type': 'invalid_email'
                }, status=400
            )

        if User.objects.filter(email_address=email_address).exists():
            
            if PasswordReset.objects.filter(user__email_address=email_address).exists():
                
                PasswordReset.objects.filter(user__email_address=email_address).delete()
                         
            code = send_verification_code(email_address, 'Password reset', "Here's your password reset code")
            
            user = User.objects.get(email_address=email_address)
            
            reset_user = PasswordReset.objects.create(user = user, code=code, code_sent_at=timezone.now())
                        
            reset_user.save()
            
            return JsonResponse(
                {
                    'status': 'success',
                }, status=200
            )
        else:
            return JsonResponse(
                {
                    'message': "Email doesn't exist",
                    'type': 'wrong_email'
                }, status=400
            )
    else:
        return JsonResponse(
            {
                'message': 'Invalid request method',
                'type': 'invalid_method'
            }, status=405
        )


@csrf_exempt
def resetPassword(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))

        email_address = str(data.get('email_address'))
        entered_code = str(data.get('code'))
        new_password = str(data.get('new_password'))
        
        reset_user = PasswordReset.objects.get(user__email_address = email_address)
        
        user = reset_user.user
        
        if reset_user.code == entered_code and not is_code_expired(reset_user.code_sent_at) and user.password != new_password:
            
            user.password = str(new_password)
            
            user.save()
            
            reset_user.delete()
            
            return JsonResponse(
                {
                    'status': 'success'
                }, status = 200) 
        
        elif user.password == new_password:
            return JsonResponse(
                {          
                    'type': 'the same passsword'
                }, status = 400)
            
        elif reset_user.code != entered_code:
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