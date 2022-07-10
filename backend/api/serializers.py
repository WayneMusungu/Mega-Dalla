from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from core.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields =('username','email', 'is_customer','is_vendor','password')
        extra_kwargs = {'password':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields ='__all__'
        
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vendor
        fields ='__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields="__all__"
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Order
        fields="__all__"
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transaction
        fields="__all__"
        
        
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False
    )
    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            raise serializers.ValidationError("Invalid User Credentials")
        attrs['user'] =user
        
        return attrs
  