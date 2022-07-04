from pydoc import stripid
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import DetailView
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
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

@login_required
def logout_user(request):

    return render(request,'welcome.html')




def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout") 
    
class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")

    
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripid.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")
