from django.urls import path
from . import views



app_name = 'payments'
urlpatterns=[
    path('initiate-payment/',views.initiate_payment, name='initiate_payment'),
    path('callback/',views.callback_uri, name='callback'),
    
    
]