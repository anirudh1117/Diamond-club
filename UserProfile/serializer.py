from rest_framework import  serializers
#from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
import re 


class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            #print('here '+email_or_username)
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
  
            if(re.search(regex,email_or_username)):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )
                email_or_username = user_request.username
                print(email_or_username)
            

            user = authenticate(username=email_or_username, password=password)
            #print(email_or_username)
            #print(password)

            #if user:
             #   if not user.is_active:
              #      return None
                    #msg = _('User account is disabled.')
                    #raise exceptions.ValidationError(msg)
            #lse:
             #   return None
                #msg = _('Unable to log in with provided credentials.')
                #raise exceptions.ValidationError(msg)
        #else:
         #   return None
            #msg = _('Must include "email or username" and "password"')
            #raise exceptions.ValidationError(msg)

        attrs['user'] = user
        
        return attrs


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']



class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')

            token12 = Token.objects.get(key=token)
            if not token12:
                raise AuthenticationFailed('The reset link is invalid', 401)
            password=make_password(password,hasher='default')
            user12 = User.objects.filter(username__exact=token12.user).update(password=password)
            #user12.password = password
            #print(user12.get_password)
            #user12.save()
            print(user12)
            
            #print(user12.password)
            return (user12)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)




   