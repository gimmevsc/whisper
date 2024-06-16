from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from register.models import *
import json

def chat(request):
    chat_group = get_object_or_404(ChatGroup, group_name = "chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message')
        username = data.het('sender')
        author = User.objects.get(username=username)
        group = ChatGroup.objects.create(group=chat_group, author = author, body = message)
        group.save()
    
    return JsonResponse(
                {
                    'status': 'success',
                    'messages': chat_messages, 
                }, status=200
            )