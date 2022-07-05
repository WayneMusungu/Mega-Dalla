from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


router = DefaultRouter()
router.register('items', views.ItemViewset, basename='items')
router.register('profile',views.ProfileViewset, basename='profile')
router.register('orderitem', views.OrderItemViewset, basename='orderitem')
router.register('order', views.OrderViewset, basename='order')
router.register('address', views.AddressViewset, basename='address')
router.register('payment', views.PaymentViewset, basename='payment')
router.register('coupon', views.CouponViewset, basename='coupon')
router.register('refund', views.RefundViewset, basename='refund')

urlpatterns=[
    path('signup/',views.CreateUserView.as_view(),name='signup'),
    path('login/',views.LoginView.as_view(),name='login')
]

urlpatterns += router.urls