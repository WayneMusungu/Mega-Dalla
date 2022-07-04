from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile
from core.forms import UserProfileForm

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

@login_required
def logout_user(request):

    return render(request,'welcome.html')