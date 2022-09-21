
from lib2to3.pgen2 import token
from rest_framework import serializers
from authentication.models import User, TwoStepAuthModel
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators

import pyotp
import datetime

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



class OTPValidator:

    def __init__(self,data):
        self.inputOtp = data["otp"]
        self.userEmail = data["email"]

    def validate_otp(self):
        validation_output = dict()

        otpSecret = "base32secret3232"
        activeUserOtp = pyotp.TOTP(otpSecret, interval= 60)

        try:
            self.user = User.objects.filter(email=self.userEmail).first()
            tokenObject = TwoStepAuthModel.objects.filter(user= self.user).first()
            userToken = tokenObject.token
            userOtp = tokenObject.userOtp
            TwoStepAuthModel.objects.filter(token = tokenObject.token).delete()
        except Exception as e:
            validation_output["message"] = "User Invalid / OTP Expired"
            return validation_output, 401

        if(activeUserOtp.verify(self.inputOtp) and self.inputOtp == userOtp):
            validation_output["message"] = "Validation Successful"
            validation_output["token"] = userToken
            return validation_output, 200
            
        validation_output["message"] = "incorrect OTP"
        return validation_output, 400
