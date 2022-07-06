from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, User, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.utils.translation import gettext as _

# from core import models

# Register your models here.


class UserAdmin(BaseUser):
    ordering = ['id']
    list_display=   ['id', 'username', 'email', 'name']
    list_display_links=['id','email']
    fieldsets= (
        (None, {'fields': ('username', 'email','password',)}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Imp dates'), {'fields': ('last_login',)})   
    )
    add_fieldsets= (
        (None, {
            'class': ('wide'),
            'fields': ('name', 'email', 'password1','password2',)
        }),
    )
    


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(User,UserAdmin)
