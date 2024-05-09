from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def registerUser(request):
    if request.GET:
        print(request.GET)
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    response_data = {
        'username': username,
        'password': int(password)
                     }
    return JsonResponse(response_data)

def categories(request, catid):
    return HttpResponse(f"<h1>Category {catid}</h1>")

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Page Not Found</h1>')