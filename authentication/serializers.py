from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']

    def create(self, validated_data):  
        createUsers = get_user_model() 
        user = createUsers.objects.create_user(email=validated_data['email'],
                                 password=validated_data['password'])
        user.save()

        return user


    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)
         
        password = data.get('password')
         
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
         
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
          
        return super(CreateUserSerializer, self).validate(data)


# class LoginSerializer():