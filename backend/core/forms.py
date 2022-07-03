from dataclasses import field
from django.contrib.auth.models import User
from django import forms
from . models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','phone_number', 'fax_number']