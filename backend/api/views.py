from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AddressSerializer, CouponSerializer, ItemSerializer, OrderItemSerializer, OrderSerializer, PaymentSerializer, RefundSerializer, UserSerializer, UserProfileSerializer, VendorSerializer

from core.models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, User, UserProfile, Vendor

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
  
class ItemViewset(viewsets.ModelViewSet):
    permissions= IsAuthenticated
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get(request):
        user = request.user
        queryset = UserProfile.objects.filter(user_id=user.id)
        return queryset
    
class VendorViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def get(request):
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
class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
class  CouponViewset(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class= CouponSerializer
    
class RefundViewset(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class= RefundSerializer
    
    
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