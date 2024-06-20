from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email = validated_data['email_address'],
            username = validated_data['username'],
            password = validated_data['password']
        )
        return super().create(validated_data)
    
    class Meta:
        model = get_user_model()
        fields = ['email_address', 'username', 'password']
        extra_kwargs = {'password': {'write_only':True}}