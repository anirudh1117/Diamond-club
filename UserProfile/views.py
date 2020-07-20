from django.shortcuts import render
from .models import Profile
from dal import autocomplete
from django.contrib.auth.models import User
from .serializer import AuthCustomTokenSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
# Create your views here.


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
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

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class Logout(APIView):
    # print('here hello')
    def get(self, request, format=None):
        # print(request.data)
        key = request.data['token']
        if Token.objects.filter(key=key).exists():
            Token.objects.get(key=key).delete()
            content = {
                "Message": "succesfully logout"
            }
        else:
            content = {
                "Message": "wrong token"
            }
        return Response(content, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            current_site = get_current_site(request)
            message = render_to_string('Users/password_reset_email.html', {
                'user': user, 'domain': current_site.domain,
                'token': token.key,
            })
            mail_subject = 'Password Reset'
            email = EmailMessage(mail_subject, message, to=[email])
            email.send()
        else:
            Response({'Failure': 'Email is not registered!!'},
                     status.HTTP_404_NOT_FOUND)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



#class UserAutoComplete(autocomplete.Select2QuerySetView):
#    def get_queryset(self):
#        if not self.request.user.is_authenticated:
#            return User.objects.none()
#
#        qs = User.objects.all()
#
#        if self.q:
#            qs = qs.filter(username__istartswith=self.q)

#        return qs
