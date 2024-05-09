from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from re import match

from .models import User

def is_valid_email(email):
    regex = r'^.+@.+$'
    if match(regex, email):
        return True
    return False

def registerUser(request):
    
    if request.method == 'GET':
        
        username = request.GET.get('username').lower()
        email_address = request.GET.get('email_address').lower()
        password = request.GET.get('password')
        
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
                    'message': 'empty field'
                })

    else:
        return JsonResponse(
                {
                    'status': 'error',
                    'message': 'bad request'
                })
    
def categories(request, catid):
    return HttpResponse(f"<h1>Category {catid}</h1>")

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Page Not Found</h1>')