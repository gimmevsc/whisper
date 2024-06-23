from django.db.models import Q
from chat.models import Participant
from register.models import User
from base64 import b64encode

def get_users_with_shared_chats(base_user):
    # Get all participants related to chats where base_user is involved
    base_user_participants = Participant.objects.filter(chat__in=base_user.participant_set.values_list('chat', flat=True))
    
    # Get all users who are participants in these chats, excluding base_user
    users_with_shared_chats = User.objects.filter(
        participant__in=base_user_participants
    ).exclude(
        user_id=base_user.user_id
    ).distinct()
    
    return users_with_shared_chats



def get_avatar_base64(user):
    if user.profile_picture:
        with open(user.profile_picture.path, "rb") as image_file:
            return b64encode(image_file.read()).decode('utf-8')
    return None