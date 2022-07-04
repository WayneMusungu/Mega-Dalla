from django.shortcuts import render
from django.shortcuts import render,redirect
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