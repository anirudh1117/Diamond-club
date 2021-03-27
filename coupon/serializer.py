from rest_framework import  serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed,NotFound,MethodNotAllowed
from .models import AllCoupon,CouponHistory
from UserProfile.models import Profile

class CouponSerializer(serializers.Serializer):
    card_Number = serializers.IntegerField(required= True)
    card_valid = serializers.DateField(required= True)
    token = serializers.CharField(min_length=1)

    def validate(self,attrs):
        num = attrs.get('card_Number')
        exp = attrs.get('card_valid')
        token = attrs.get('token')
        if Token.objects.filter(key=token).exists():
            token12 = Token.objects.get(key=token)
            profile = Profile.objects.get(user__exact=token12.user)
            if AllCoupon.objects.filter(card_Number=num,card_valid=exp).exists():
                allcoupon = AllCoupon.objects.get(card_Number=num,card_valid=exp)
                print(CouponHistory.objects.filter(username=token12.user))
                if not CouponHistory.objects.filter(username=token12.user,card_number=allcoupon.card_Number).exists():
                    CouponHistory.objects.create(username=token12.user,card_number=allcoupon.card_Number,partner_name=profile.partner_name)
                    attrs['message']='success'
                else:
                    raise MethodNotAllowed('Coupon card already scanned by partner')
            else:
                raise NotFound('Coupon card doesnot exist')
        else:
            raise AuthenticationFailed('The token is invalid', 401)
        return attrs

class CouponHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username',read_only=True)
    class Meta:
        model = CouponHistory
        fields = ['id','username','card_number','partner_name','scannedAt']


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(
        min_length=1, write_only=True)
    def validate(self,attrs):
        token = attrs.get('token')
        if not Token.objects.filter(key=token).exists():
            raise AuthenticationFailed('The token is invalid', 401)
        token12 = Token.objects.get(key=token)
        attrs['token']=token12
        
        return attrs
