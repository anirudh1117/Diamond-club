from django.contrib import admin
from .models import Profile
from .forms import EmailForm
from django.contrib.auth.models import User, Group
from django import forms
import selectable.forms as selectable
from .lookups import UserLookup
from dal import autocomplete
from django.utils import timezone
from django.utils.html import format_html
from django.conf.urls import url
# Register your models here.
from django.urls import reverse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import csv


# admin.site.unregister(Token)


class ProfileAdminForm(forms.ModelForm):
    # user = selectable.AutoCompleteSelectField(lookup_class=UserLookup, allow_new=True)

    class Meta:
        model = Profile
        fields = ('__all__')
        widgets = {
            'user': autocomplete.ModelSelect2(url='User-autocomplete')
        }


class ProfileAdmin(admin.ModelAdmin):
    mreciever=[]
    list_display = ('id', 'user', 'phoneNo','discount_provided',
                    'days_since_joined', 'profile_actions')
    list_filter = ('Business_Type','date_joined',)
    search_fields = ('user__username',)
    date_hierarchy = 'date_joined'
    list_per_page = 20
    list_display_links = ('id','user',)
    list_editable = ('discount_provided',)
    actions = ['Send_Group_mail','export_profile', ]

    def days_since_joined(self, Profile):
        diff = timezone.now()-Profile.date_joined
        return diff.days

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [url(
            r'^send-mail/(\d+)/$', self.admin_site.admin_view(self.send_email), name='send-email'),
            url(
            r'^send-group-mail/$', self.admin_site.admin_view(self.Send_Group_mail2), name='send-group-email'),
            url(
            r'^send-reset-mail/(\d+)/$', self.admin_site.admin_view(self.Send_reset_mail), name='send-reset-email'),
        ]

        return custom_url+urls

    def profile_actions(self, obj):
        return format_html('<button style="background-color: #008CBA;"> <a style="color: white;" href="{}">Send Email</a></button>&nbsp;'
        '<button style="background-color: #008CBA;"> <a style="color: white;" href="{}">Password Reset Email</a></button>',
        reverse('admin:send-email', args=[obj.pk]),
        reverse('admin:send-reset-email', args=[obj.pk]),
        )
    profile_actions.short_description = 'Profile Actions'
    profile_actions.allow_tags = True

    def send_email(self, request, pk):
        profile = Profile.objects.get(id=pk)
        user12 = get_object_or_404(User, username=profile.user)
        # print(user12.email)
        reciever = user12.email
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['Subject']
                message = form.cleaned_data['Message']
                email = EmailMessage(subject, message, to=[reciever])
                email.content_subtype = "html"
                email.send()
                return redirect('/admin/UserProfile/profile/')
        else:
            form = EmailForm()
            data = {'test': 'test',
                    'opts': Profile._meta,
                    'change': True,
                    'is_popup': False,
                    'save_as': False,
                    'has_delete_permission': False,
                    'has_add_permission': False,
                    'has_change_permission': False,
                    'add': 'add',
                    'has_view_permission': False,
                    'has_editable_inline_admin_formsets': False,
                    'form': form,
                    'reciever': reciever
                    }
            return TemplateResponse(request, 'admin/send-email.html', data)

    def Send_reset_mail(self,request,pk):
        profile = Profile.objects.get(id=pk)
        user = get_object_or_404(User, username=profile.user)
        # print(user12.email)
        token, created = Token.objects.get_or_create(user=user)
        current_site = get_current_site(request)
        message = render_to_string('Users/password_reset_email2.html', {
                'user': user, 'domain': current_site.domain,
                'token': token.key,
                'pk':pk  
            })
        mail_subject = 'Password Reset'
        
        print(user.email)
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html"
        print(email)
        email.send()
        print(email)
        return redirect('/admin/UserProfile/profile/')


    def Send_Group_mail(self, request, queryset):
        reciever = []
        print(queryset)
        for dek in queryset:
            user = get_object_or_404(User, username=dek.user)
            reciever.append(user.email)
        self.mreciever=reciever
        form = EmailForm()
        print(1)
        data = {'test': 'test',
            'opts': Profile._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False,
            'add': 'add',
            'has_view_permission': False,
            'has_editable_inline_admin_formsets': False,
            'form': form,
            'reciever':reciever
            }
        return TemplateResponse(request, 'admin/send-mail2.html', data)


    def Send_Group_mail2(self,request):
        if request.method == 'POST':
            form = EmailForm(request.POST)
            print('Here')
            if form.is_valid():
                
                subject = form.cleaned_data['Subject']
                message = form.cleaned_data['Message']
                print(self.mreciever)
                email = EmailMessage(
                subject, message, bcc=self.mreciever)
                email.content_subtype = "html"
                print('email ')
                email.send()
                print('email ')
                return redirect('/admin/UserProfile/profile/')

        form = EmailForm()
        print(1)
        data = {'test': 'test',
            'opts': Profile._meta,
            'change': True,
            'is_popup': True,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False,
            'add': 'add',
            'has_view_permission': False,
            'has_editable_inline_admin_formsets': False,
            'form': form,
            'reciever': reciever
            }
        return TemplateResponse(request, 'admin/send-mail2.html', data)


    Send_Group_mail.short_description = 'Send Mail to group'


    def export_profile(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profile.csv"'
        writer = csv.writer(response)
        writer.writerow(['Id', 'Username', 'Email', 'Date Joined', 'Business Type'])
        books = queryset.values_list('id', 'user__username', 'email', 'date_joined', 'Business_Type')
        for book in books:
            writer.writerow(book)
        return response
    export_profile.short_description = 'Export to csv'


admin.site.register(Profile, ProfileAdmin)
#admin.site.unregister(Token)
