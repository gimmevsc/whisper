from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    if request.GET:
        print(request.GET)
    
    return HttpResponse(f"{request.GET['name']} is cool")

def categories(request, catid):
    return HttpResponse(f"<h1>Category {catid}</h1>")

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Page Not Found</h1>')