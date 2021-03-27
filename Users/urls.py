from django.urls import path
from django.conf.urls import url
from .views import RegisterAPI,LoginAPI,LogoutAPI,Check_UsernameOrEmail,FacebookSocialAuthView, GoogleSocialAuthView
urlpatterns = [
	url('register', RegisterAPI.as_view()),
	url('login', LoginAPI.as_view()),
	url('logout', LogoutAPI.as_view()),
	url('check-username-email',Check_UsernameOrEmail.as_view()),
	path('google', GoogleSocialAuthView.as_view()),
    path('facebook', FacebookSocialAuthView.as_view()),

	]
