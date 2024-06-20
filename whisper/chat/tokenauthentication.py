import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, token):
        # token = self.extract_token(request=request)
        # if token in None:
        #     return None 
        # try:s
        playload = jwt.decode(token, settings.SECRET_KEY, 'HS256')
        # self.verify_token(playload=playload)
        
        user_id = playload['user_id']
        user = User.objects.get(user_id=user_id)
        return user
        
        # except(InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
        #     raise AuthenticationFailed("Invalid token")
        
    # def verify_token(self, playload):
    #     if "exp" not in playload:
    #         raise IndentationError("Token has no expiration")    

    #     exp_timestamp = playload['exp']
    #     current_timestamp = datetime.utcnow().timestamp()
    
    #     if current_timestamp < exp_timestamp:
    #         raise ExpiredSignatureError("Token has expired")
        
    def extract_token(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.starstwith('Bearer '):
            return auth_header.split(" ")[1]
        return None
    
    
    @staticmethod
    def generate_token(playload):
        expiration = datetime.utcnow() + timedelta(hours=24)
        playload['exp'] = expiration
        token = jwt.encode(playload, settings.SECRET_KEY, 'HS256')
        return token
    
        