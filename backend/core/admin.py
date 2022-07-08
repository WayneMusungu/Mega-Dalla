from django.contrib import admin
from .models import Item, OrderItem, Order, Address, UserProfile, Vendor,User
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.utils.translation import gettext as _


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    'payment',
                    
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'payment',
        
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   ]
    search_fields = [
        'user__username',    
    ]
   



class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'billing_address',
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
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Vendor)
