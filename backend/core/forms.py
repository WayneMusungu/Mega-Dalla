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
)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','phone_number', 'fax_number']
        
        
class RegistrationForm( UserCreationForm, forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    email=forms.EmailField(max_length=100, required=True)
    class Meta:
        model = get_user_model()
        fields =('username','email', 'is_customer','is_vendor')
        extra_kwargs = {'password':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password=forms.CharField(max_length=20, widget=forms.PasswordInput)
    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
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
    
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))



