from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from cloudinary.models import CloudinaryField
from django.shortcuts import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

from payments.models import Transaction

from payments.models import Transaction

CATEGORY_CHOICES = (
    ('C', 'Clothes'),
    ('E', 'Electronics'),
    ('G', 'Groceries'),
    ('J', 'Jewelry'),
    ('S', 'Stationery')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class User(AbstractUser):
    is_customer= models.BooleanField('Customer',default=True)
    is_vendor= models.BooleanField('Vendor',default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    bio = models.CharField(max_length=250)
    email = models.EmailField(null=True, max_length=250)
    phone_number = PhoneNumberField()
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, dispatch_uid="customer", **kwargs):
        if instance.is_customer:
            if created:
                UserProfile.objects.get_or_create(user = instance)            
        
    @receiver(post_save, sender=User)
    def save_admin(sender, instance, **kwargs):
        if instance.is_customer:
            instance.customer.save()
    
    def save_profile(self):
            self.save()
            
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    bio = models.CharField(max_length=250)
    email= models.EmailField(max_length=100)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_vendor(sender, instance, created, dispatch_uid="vendor", **kwargs):
        if instance.is_vendor:
            if created:
                Vendor.objects.get_or_create(user = instance)            
        
    @receiver(post_save, sender=User)
    def save_admin(sender, instance, **kwargs):
        if instance.is_vendor:
            instance.vendor.save()
    
    def save_profile(self):
            self.save()


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = CloudinaryField('image')
    # amount = models.FloatField()
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Transaction, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)


    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name_plural = 'Addresses'
