
from django.urls import path, include
from . import views
from django_registration.backends.one_step.views import RegistrationView
from .views import ItemDetailView,CheckoutView
from .views import ItemDetailView, OrderSummaryView, remove_single_item_cart


urlpatterns=[
    path('',views.welcome, name='welcome'),
    path('home/',views.home, name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('add-to-cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name="remove-from-cart"),
    path('remove-single-item-cart/<slug>',remove_single_item_cart, name='remove-single-item-cart'),
    path('profile-update/',views.update_profile, name='update_profile'),
    path('order-summery/',OrderSummaryView.as_view(), name='order-summery'),

    # path('accounts/', include('Account.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include(('django.contrib.auth.urls', 'core'), namespace='login')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_user, name='logout'),

]
