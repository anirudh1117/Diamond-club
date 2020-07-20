from django.urls import path
from dal import autocomplete
from .models import Profile
from django.conf.urls import url
from rest_framework.authtoken import views
from .views import ObtainAuthToken,Logout,RequestPasswordResetEmail,SetNewPasswordAPIView

urlpatterns = [
    #path('User-autocomplete/$',autocomplete.Select2QuerySetView.as_view(model=Profile),name='User-autocomplete'),
    #url(r'^User-autocomplete/$',UserAutoComplete.as_view(),name='User-autocomplete'),
    url(r'^login/$', ObtainAuthToken.as_view(), name='get_user_auth_token'),
    url(r'^logout/$', Logout.as_view()),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/',
         SetNewPasswordAPIView.as_view(), name='password-reset-confirm'),
    
    
    
    ]