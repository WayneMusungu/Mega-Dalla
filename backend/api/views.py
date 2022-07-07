from rest_framework import generics, viewsets
from .serializers import AddressSerializer, ItemSerializer, OrderItemSerializer, OrderSerializer, UserProfileSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status

from core.models import Item, OrderItem, Order, Address,  UserProfile

# Create your views here.

# class CreateUserView(generics.CreateAPIView):
#     serializer_class = UserSerializer

# class LoginView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializer

#     def post(self, request, *args,**kwargs):
#         serializers = self.serializer_class(data=request.data,context={'request':request})
#         serializers.is_valid(raise_exception=True)
#         user = serializers.validated_data['user']
#         token,created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'username': user.username,
#             'id': user.id,
#             'email': user.email,
#             'name': user.name,
#         })
        
class ItemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get(request):
        user = request.user
        queryset = UserProfile.objects.filter(user_id=user.id)
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
