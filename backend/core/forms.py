from dataclasses import field
from django.contrib.auth.models import User
from django import forms
from . models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('C', 'Credit'),
    ('P', 'PayPal'),
    ('D', 'Debit'),
    ('S', 'Stripe'),
    ('M', 'Mpesa'),
    
)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','phone_number']
        
        
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
class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)
    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    
# 

    
# class PaymentForm(forms.Form):
#     stripeToken = forms.CharField(required=False)
#     save = forms.BooleanField(required=False)
#     use_default = forms.BooleanField(required=False)



