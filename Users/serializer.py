from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
import re
from . import google, facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed

GOOGLE_CLIENT_ID = '461998924717-nlhg007hcr65ukd4ldsol52okh9uc18h.apps.googleusercontent.com'
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)


    class Meta:
        model = User
        fields = ('username','first_name','last_name','password','email')


    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
             password=validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])
        user.password = ""
        return user



class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
  
            if(re.search(regex,email_or_username)):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )
                if user_request:
                    email_or_username = user_request.username
                
            

            user = authenticate(username=email_or_username, password=password)

        attrs['user'] = user
        
        return attrs

class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email  = None
            if 'email' in user_data.keys():
                email = user_data['email']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            name = user_data['name']
            provider = 'facebook'
            print(user_data)
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name,
                first_name=first_name,
                last_name=last_name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        print(user_data)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name,first_name=first_name,last_name=last_name)





        
