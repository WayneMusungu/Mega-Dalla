from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from payments.models import Transaction

from .serializers import AddressSerializer, ItemSerializer, LoginSerializer, OrderItemSerializer, OrderSerializer,  TransactionSerializer, UserSerializer, UserProfileSerializer, VendorSerializer

from core.models import Item, OrderItem, Order, Address, UserProfile, Vendor

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
class LoginView(APIView):

    serializer_class = LoginSerializer

    def post(self, request, *args,**kwargs):
        serializers = self.serializer_class(data=request.data,context={'request':request})
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
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