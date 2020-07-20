from dal import autocomplete
from django.contrib.auth.models import User
from django import forms
from .models import Profile
import selectable.forms as selectable
from .lookups import UserLookup
from ckeditor.fields import RichTextFormField


class ProfileForm(forms.ModelForm):
    # user = forms.ModelChoiceField(
    #    queryset=User.objects.all(),
    #    widget=autocomplete.ModelSelect2(
    #    	url='User-autocomplete')
   # )
    class Meta:
        model = Profile
        fields = ('__all__')
        widgets = {
            'user': selectable.AutoCompleteSelectWidget(lookup_class=UserLookup),
        }


class EmailForm(forms.Form):
    Subject = forms.CharField(label='Subject', max_length=100, min_length=5,
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control',
                                         'id': 'subject',
                                         'placeholder': 'Type Something....'}))
    Message = RichTextFormField(widget=forms.TextInput(
                                  attrs={'class': 'form-control',
                                         'id': 'message',
                                         'placeholder': 'Type Something....'}))
    
    class Meta:
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['Subject'].widget.attrs['cols'] = 20
        self.fields['Subject'].widget.attrs['rows'] = 4
