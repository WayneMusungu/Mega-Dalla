
from django.urls import path, include
from . import views
from django_registration.backends.one_step.views import RegistrationView
<<<<<<< HEAD
from .views import ItemDetailView, OrderSummaryView, remove_single_item_cart,update_profile, CheckoutView
=======
from .views import CheckoutView, ItemDetailView, OrderSummaryView, remove_single_item_cart,update_profile
>>>>>>> a60129a9cc93f7bcfdade7a65a69f17b7a29f30b


urlpatterns=[
    path('',views.welcome, name='welcome'),
    path('home/',views.home, name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name="remove-from-cart"),
    path('remove-single-item-cart/<slug>',remove_single_item_cart, name='remove-single-item-cart'),
    path('profile-update/',update_profile, name='update_profile'),
    path('order-summery/',OrderSummaryView.as_view(), name='order-summery'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),


    # path('accounts/', include('Account.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include(('django.contrib.auth.urls', 'core'), namespace='login')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_user, name='logout'),

]
