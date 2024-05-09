from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from register.models import User

def registerUser(request):
    
    if request.method == 'GET':
        
        username = request.GET.get('username').lower()
        email_address = request.GET.get('email_address').lower()
        password = request.GET.get('password')

        if username and email_address and password:
            
            if User.objects.filter(email=email_address).exists():
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Email address already exists',
                        'type': 'email'
                    })
            
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {   'status': 'error',
                        'message': 'Username already exists',
                        'type': 'username'
                    })
                
            user = User.objects.create_user(username=username, email=email_address, password=password)

            user.created_at = timezone.now()
            user.updated_at = timezone.now()
            
            user.save()

            return JsonResponse(
                {   
                    'status': 'success'
                })
        else:
            return JsonResponse(
                {
                    'status': 'error'
                })

    else:
        return JsonResponse(
                {
                    'status': 'error'
                })
    
def categories(request, catid):
    return HttpResponse(f"<h1>Category {catid}</h1>")

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Page Not Found</h1>')