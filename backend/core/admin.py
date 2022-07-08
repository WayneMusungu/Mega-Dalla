from django.contrib import admin
from .models import Item, OrderItem, Order, Address, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.utils.translation import gettext as _

# from core import models

# Register your models here.


# class UserAdmin(BaseUser):
#     ordering = ['id']
#     list_display=   ['id', 'username', 'email', 'name']
#     list_display_links=['id','email']
#     fieldsets= (
#         (None, {'fields': ('username', 'email','password',)}),
#         (_('Personal info'), {'fields': ('name',)}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
#         (_('Imp dates'), {'fields': ('last_login',)})   
#     )
#     add_fieldsets= (
#         (None, {
#             'class': ('wide'),
#             'fields': ('name', 'email', 'password1','password2',)
#         }),
#     )
    




class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
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
# admin.site.register(User,UserAdmin)
