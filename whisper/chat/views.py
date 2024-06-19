from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from chat.models import ChatModel
from register.models import *
import json
from django.http import JsonResponse



def chatPage(request, room_name):
    messages = ChatModel.objects.filter(thread_name=room_name).order_by('timestamp')
    messages_list = list(messages.values('sender', 'message', 'timestamp'))
    return JsonResponse(messages_list, safe=False)
#     user_obj = User.objects.get(username=username)
#     users = User.objects.exclude(username=request.user.username)

#     if request.user.user_id > user_obj.user_id:
#         thread_name = f'chat_{request.user.id}-{user_obj.id}'
#     else:
#         thread_name = f'chat_{user_obj.id}-{request.user.id}'
#     message_objs = ChatModel.objects.filter(thread_name=thread_name)
#     return render(request, 'main_chat.html', context={'user': user_obj, 'users': users, 'messages': message_objs})
# def chat(request):
#     chat_group = get_object_or_404(ChatGroup, group_name = "chat")
#     chat_messages = chat_group.chat_messages.all()[:30]
    
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         message = data.get('message')
#         username = data.het('sender')
#         author = User.objects.get(username=username)
#         group = ChatGroup.objects.create(group=chat_group, author = author, body = message)
#         group.save()
    
#     return JsonResponse(
#                 {
#                     'status': 'success',
#                     'messages': chat_messages, 
#                 }, status=200
#             )