from django.utils import timezone
import re
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

from map.models.user import User

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Login failed, wrong email or password")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Login failed, wrong email or password")
        return user
    
    
class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(max_length=256)
    newPassword = serializers.CharField(max_length=256)
    
class RespondToNewPasswordChallengeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=2048)
    email = serializers.EmailField()

class ResendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class NewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)