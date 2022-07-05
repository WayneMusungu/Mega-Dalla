from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, User, UserProfile
from core.forms import UserProfileForm,RegistrationForm,LoginForm

from rest_framework import generics, viewsets
from .serializers import AddressSerializer, CouponSerializer, ItemSerializer, OrderItemSerializer, OrderSerializer, PaymentSerializer, RefundSerializer, UserSerializer, UserProfileSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status

# Create your views here.
# def welcome(request):
#     return HttpResponse('Welcome to the login page')
def welcome(request):

    return render(request, 'welcome.html')


@login_required
def home(request):
    items = Item.objects.all()
    print(items)
    context = {
        'items': items
    }
    return render(request, 'home.html', context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if item is in cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "Item quantity was updated")

        else:
            messages.success(request, "Item was add to your cart")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        messages.success(request, "This item was add to your cart")

        order.items.add(order_item)

    return redirect("core:product", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        print('order', order)
        # Check if item is in cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.success(request, "This item was removed from your cart")
            return redirect("core:product", slug=slug)
        else:
            messages.success(request, "This item is not in your cart")
            return redirect("core:product", slug=slug)
    else:
        # display message that order doesnt exist
        messages.danger(request, "Item doesnt exist")
        return redirect("core:product", slug=slug)

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    form = UserProfileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            details = form.save(commit=False)
            details.user = request.user
            details.save()
            return redirect ('home')
        else:
            form = UserProfileForm()
    return render(request, 'profile-update.html', {'form': form})

def register(request):
    form = RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user =  form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            form.save()
        return redirect(login_user)
    return render(request, 'auth/register.html',locals())

def login_user(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            usern=form.cleaned_data['email']
            passw=form.cleaned_data['password']
            user=authenticate(request,username=usern,password=passw)
            if user is not None:
                login(request,user)
                return redirect('core:home')
            else:
                return HttpResponse('Such a user does not exist')
        else:
            return HttpResponse("Form is not Valid")
    
    return render(request,'auth/login.html',locals())

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('/')
