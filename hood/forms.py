from django import forms
from .models import Profile
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['']


class AddHoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        exclude = ['user_profile', 'profile']