from functools import partial
import profile
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from payments.models import Transaction

from .serializers import AddressSerializer, ItemSerializer, LoginSerializer, OrderItemSerializer, OrderSerializer,  TransactionSerializer, UserSerializer, UserProfileSerializer, VendorSerializer

from core.models import Item, OrderItem, Order, Address, User, UserProfile, Vendor

from api import serializers
from django.contrib.auth import login

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args,**kwargs):
        # serializers = self.serializer_class(data=request.data,context={'request':request})
        serializers=AuthTokenSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        refresh = RefreshToken.for_user(user)
        login(request, user)
        
        return Response({
            'username': user.username,
            'id': user.id,
            'email': user.email,
            'is_vendor':user.is_vendor,
            'is_customer':user.is_customer,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class ItemViewset(viewsets.ModelViewSet):
    permissions= IsAuthenticated
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ProfileViewset(generics.RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    # queryset = UserProfile.objects.all()  
    serializer_class = UserProfileSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        print(profile)
        data = UserProfileSerializer(profile, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user= request.user
        profile = UserProfile.objects.get(user=user)
        print(profile)
        serializer = UserProfileSerializer(profile,data=request.data, context={'request': request},partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)
    
class VendorViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Vendor.objects.filter(user_id=user.id)
        return queryset

class OrderItemViewset(viewsets.ModelViewSet):
    queryset= OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class= AddressSerializer
    
    # def update_address(self, serializer):
    #     serializer.save(user=self.request.user)

class TransactionViewset(viewsets.ModelViewSet):
    queryset= Transaction.objects.all()
    serializer_class= TransactionSerializer

class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # print(request.data)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)