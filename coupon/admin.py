from django.contrib import admin
from .models import AllCoupon, CouponHistory
#from .views import add_coupon
#from django.conf.urls import url
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
# Register your models here.

class IsVeryFilter(admin.SimpleListFilter):
    title = 'filter by status'
    parameter_name = 'filter by status'

    def lookups(self, request, model_admin):
        return (
            ('Expired', 'Expired'),
            ('Not Expired', 'Not Expired'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Expired':
            return queryset.exclude(card_valid__gte=timezone.now().date())
        elif value == 'Not Expired':
            return queryset.filter(card_valid__gte=timezone.now().date())
        return queryset







class CouponAdmin(admin.ModelAdmin):
    list_display = ('id','card_Number','card_valid','card_user_id','card_user_name','status')
    list_filter = ('card_valid',IsVeryFilter)
    #list_display_links = ('id','card_Number','card_valid')
    list_per_page = 20
    date_hierarchy = 'card_valid'
    ordering = ('-card_valid',)
    search_fields = ('card_Number',)

    def get_urls(self):
        urls = super().get_urls()
        urls.pop(1)
        #urls.insert(1,url('/',self.admin_site.admin_view(self.addCoupon),name='add-coupon'))
        #print('sd',urls)
        return urls

    def has_add_permission(self, request):
        return False
    def status(self, AllCoupon):
        diff = AllCoupon.card_valid - timezone.now().date()
        if diff.days < 0:
            return 'Expired ' +str(-diff.days)+' days ago'
        else :
            return str(diff.days)+' days left'

    def status_exp(self,AllCoupon):
        diff = AllCoupon.card_valid - timezone.now().date()
        if diff.days < 0 :
            return 'expired'
        else:
            return 'Not expired'




admin.site.register(AllCoupon,CouponAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id','card_number','username','partner_name','scannedAt')
    list_filter = ('username','scannedAt',)
    search_fields = ('username__username','partner_name')
    list_per_page = 20
    date_hierarchy = 'scannedAt'

    def get_urls(self):
        urls = super().get_urls()
        urls.pop(1)
        return urls

    def has_add_permission(self, request):
        return False
    def has_save_permission(self, request):
        return False


admin.site.register(CouponHistory,HistoryAdmin)