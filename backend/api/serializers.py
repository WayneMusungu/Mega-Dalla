from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from core.models import *
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields =('email','username','password', 'is_active','is_staff')
#         extra_kwargs = {'password':{'write_only':True,'min_length':8}}

#     def create(self,validated_data):
#         return get_user_model().objects.create_user(**validated_data)

# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type':'password'},
#         trim_whitespace = False
#     )
#     def validate(self,attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(
#             request=self.context.get('request'),
#             email=email,
#             password=password
#         )
#         if not user:
#             raise serializers.ValidationError("Invalid User Credentials")
#         attrs['user'] =user
#         return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user','stripe_customer_id','phone_number','bio',]
        
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
