from django.urls import path
from .views import check_token,Couponhistory

urlpatterns = [
    path('check-card/',check_token.as_view(),name='check'),
    path('get-history/',Couponhistory.as_view(),name='history'),
]