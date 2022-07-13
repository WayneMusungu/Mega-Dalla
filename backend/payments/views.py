
from django.shortcuts import render, reverse
from django.utils.crypto import get_random_string
from python_flutterwave import payment
from django.http import HttpResponseRedirect, HttpResponse

from core.models import UserProfile, Order
from .models import Transaction
from django.contrib.auth.decorators import login_required


payment.token = 'FLWSECK_TEST-c705a4deea97a1a5df4f6049b8c96a07-X'

@login_required
def initiate_payment(request):
    orders = Order.objects.get(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    transaction = Transaction(user=request.user)
    transaction.trans_ref = get_random_string(12)
    transaction.save()
    
    protocol = f'https' if request.is_secure() else 'http'
    callback_url = f"{protocol}://{request.get_host()}{reverse('payments:callback')}"
    
    
    uri = payment.initiate_payment(tx_ref=transaction.trans_ref, amount=orders.get_total(), currency='KES', redirect_url=callback_url, 
                                   customer_name=request.user.username, customer_email=request.user.email, customer_phone_number=profile.phone_number
                                   , payment_options='mpesa', title='Mega Dalla',
                                   description='payment for goods')
    
    return HttpResponseRedirect(uri)
    
  


def callback_uri(request):
    tx_ref = request.GET.get('tx_ref')
    trans_id = request.GET.get('transaction_id')
    status = request.GET.get('status')
    
    transaction =Transaction.objects.get(trans_ref=tx_ref)
    
    if trans_id is None:
        
        transaction.trans_status = status
        transaction.save()
        
        return HttpResponse('Transaction failed try again')
    
    
    details = payment.get_payment_details(trans_id)
    
    print(details)
    
    transaction.trans_id = trans_id
    
    transaction.trans_status = details['status']
    
    transaction.save()
    
    return HttpResponse('Payment has been received')
