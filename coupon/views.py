from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth
from .models import AllCoupon,CouponHistory
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import parsers
from .serializer import CouponSerializer,CouponHistorySerializer,TokenSerializer
from django.http.response import JsonResponse


# Create your views here.


def add_coupon():
    re = requests.get(
        'https://diamondclubunion.com/api/cards.php?get=cards',
        auth=HTTPBasicAuth('validator', 'DCU@validator_access')
    )
    response = re.json()
    #print(re)
    for r in response:
        if AllCoupon.objects.filter(card_Number=r['card_id']).exists():
            print('already exist')
        else:
            newdate = datetime.strptime(r['card_valid'],'%d.%m.%Y')
            AllCoupon.objects.create(card_Number=r['card_id'],card_valid=newdate,card_user_name=r['user_name'],card_user_id=r['user_id'])
        #print(r['card_valid'])


class check_token(APIView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser
    )

    def post(self,request):
        add_coupon()
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message = serializer.validated_data['message']
            content={
                message:'success, Transaction can be processed'
            }
            return JsonResponse(content)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Couponhistory(APIView):
    def post(self,request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            history = CouponHistory.objects.filter(username=token.user)
            print(history.values())
            serializer12 = CouponHistorySerializer(history,many=True)
            print('ds' ,serializer12.data)
            #hi2 = list(history.values())
            #hi2 =  history.json()
            return JsonResponse(serializer12.data,safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

