from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
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
        fields = ['user','stripe_customer_id','phone_number','bio',]
        
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vendor
        fields ='__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['title','price','description','discount_price','label','slug','image']
        
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

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields=['user','amount','timestamp']
        
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields="__all__"
        
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model=Refund
        fields="__all__"