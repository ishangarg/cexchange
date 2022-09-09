from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']

    def create(self, validated_data):  
        createUsers = get_user_model() 
        user = createUsers.objects.create_user(email=validated_data['email'],
                                 password=validated_data['password'])
        user.save()

        return validated_data