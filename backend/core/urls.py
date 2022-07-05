from django.urls import path, include
from . import views
from django_registration.backends.one_step.views import RegistrationView
from .views import ItemDetailView


urlpatterns=[
    path('',views.welcome, name='welcome'),
    path('home/',views.home, name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name="remove-from-cart"),
    path('profile-update/',views.update_profile, name='update_profile'),
    # path('accounts/', include('Account.urls')),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include(('django.contrib.auth.urls', 'core'), namespace='login')),
    # path('accounts/', include('django_registration.backends.one_step.urls')),
    # path('accounts/', include(('django.contrib.auth.urls', 'core'), namespace='login')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('logout/', views.logout_user, name='logout'),
]