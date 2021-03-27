from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework.renderers import JSONRenderer
from .serializer import UserSerializer, LoginSerializer, FacebookSocialAuthSerializer, GoogleSocialAuthSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse
from django.contrib.auth.models import User

# Create your views here.


class RegisterAPI(APIView):
        parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
        #renderer_classes = (renderers.JSONRenderer)

        def post(self, request):
                print(request.data)
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                        user = serializer.save()
                        if user:
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        	


class LoginAPI(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            if user:
                token, created = Token.objects.get_or_create(user=user)
                content = {
                    'token': token.key,
                    'Message': 'success'
                }
                return Response(content)
        
            else:
                content = {
                    'Message': 'Unable to log in with provided credentials.'
                }
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutAPI(APIView):
    def get(self, request, format=None):
        key = request.data['token']
        if Token.objects.filter(key=key).exists():
            Token.objects.get(key=key).delete()
            content = {
                "Message": "succesfully logout"
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                "Message": "Token is invalid"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class Check_UsernameOrEmail(APIView):
        def get(self,request,format=None):
                username = request.data['username']
                email = request.data['email']
                a=0
                b=0
                if username=="":
                    a=0
                elif not User.objects.filter(username=username).exists():
                        a = 1
                if email=="":
                    b=0
                elif not User.objects.filter(email=email).exists():
                        b = 1
                content={
                        "username":a,
                        "email":b
                }
                
                
                return Response(content, status=status.HTTP_200_OK)





class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)