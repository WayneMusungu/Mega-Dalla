from dataclasses import field
from django.contrib.auth.models import User
from django import forms
from . models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','phone_number', 'fax_number']
        
        
class RegistrationForm( UserCreationForm, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields =('email','username', 'is_active','is_staff')
        extra_kwargs = {'password':{'write_only':True,'min_length':8}}

    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)

class LoginForm(forms.Form):
    email=forms.CharField(max_length=50)
    password=forms.CharField(max_length=20, widget=forms.PasswordInput)
    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            raise forms.ValidationError("Invalid User Credentials")
        attrs['user'] =user
        return attrs