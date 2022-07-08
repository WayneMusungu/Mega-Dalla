from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from django.urls import path


router = DefaultRouter()
router.register('items', views.ItemViewset, basename='items')
router.register('profile',views.ProfileViewset, basename='profile')
router.register('orderitem', views.OrderItemViewset, basename='orderitem')
router.register('order', views.OrderViewset, basename='order')
router.register('address', views.AddressViewset, basename='address')
router.register('transaction', views.TransactionViewset, basename='transaction')


urlpatterns=[
    path('signup/',views.CreateUserView.as_view(),name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
]

urlpatterns += router.urls
