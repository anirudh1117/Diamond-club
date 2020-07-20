from django.contrib import admin
from .models import Profile
from .forms import EmailForm
from django.contrib.auth.models import User,Group
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
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from rest_framework.authtoken.models import Token


#admin.site.unregister(Token)


class ProfileAdminForm(forms.ModelForm):
    # user = selectable.AutoCompleteSelectField(lookup_class=UserLookup, allow_new=True)

    class Meta:
        model = Profile
        fields = ('__all__')
        widgets = {
            'user': autocomplete.ModelSelect2(url='User-autocomplete')
        }


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phoneNo',
                    'days_since_joined', 'profile_actions')
    list_filter = ('user', 'date_joined',)
    search_fields = ('user__username',)
    date_hierarchy = 'date_joined'
    list_per_page = 20

    def days_since_joined(self, Profile):
        diff = timezone.now()-Profile.date_joined
        return diff.days

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [url(
            r'^send-mail/(\d+)/$', self.admin_site.admin_view(self.send_email), name='send-email')]

        return custom_url+urls

    def profile_actions(self, obj):
        return format_html('<button style="background-color: #008CBA;"> <a style="color: white;" href="{}">Send Email</a></button>', reverse('admin:send-email', args=[obj.pk]),)
    profile_actions.short_description = 'Profile Actions'
    profile_actions.allow_tags = True

    # def send_email(self, request, pk):

    #   profile = Profile.objects.get(id=pk)
    #  user12 = get_object_or_404(User, username=profile.user)
    # print(user12.email)
    #   reciever = user12.email
    #  return self.process_action(request=request, reciever=reciever)

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


admin.site.register(Profile, ProfileAdmin)
#admin.site.register(Token)

