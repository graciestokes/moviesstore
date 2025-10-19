from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    latitude = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitude', 'id': 'id_latitude'}))
    longitude = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'longitude', 'id': 'id_longitude'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'latitude', 'longitude')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__ (*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )
    def save(self, commit=True):
        user = super().save(commit)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')
        if hasattr(user, 'profile'):
            user.profile.latitude = lat
            user.profile.longitude = lon
            user.profile.save()
        return user