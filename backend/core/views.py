from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView,View
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile
from core.forms import UserProfileForm,CheckoutForm,CouponForm

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



class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")


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
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView,View 
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
            return redirect("core:order-summery")

        else:
            messages.success(request, "Item was add to your cart")
            order.items.add(order_item)
            return redirect("core:order-summery")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        messages.success(request, "This item was add to your cart")

        order.items.add(order_item)

    return redirect("core:order-summery")

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
            return redirect("core:order-summery")
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

@login_required
def logout_user(request):

    return render(request,'welcome.html')


class OrderSummaryView(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request,"you dont have an active order")
            return redirect("/")

    def get_total_item_price(self):
        return self.Quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.Quantity * self.item.discount_item

#removing a single item from cart
def remove_single_item_cart(request, slug):
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
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.remove(order_item)
            messages.success(request, "This item quantity was updated")
            return redirect("core:order-summery")
        else:
            messages.success(request, "This item is not in your cart")
            return redirect("core:product", slug=slug)
    else:
        # display message that order doesnt exist
        messages.danger(request, "Item doesnt exist")
        return redirect("core:product", slug=slug)
    
