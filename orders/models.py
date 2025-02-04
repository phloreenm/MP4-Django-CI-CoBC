# orders/models.py
from django.db import models
from django.conf import settings
import uuid
from django_countries.fields import CountryField
from products.models import Product

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    # Link the order to a user (optional but recommended for filtering orders)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    status = models.CharField(max_length=20, default='pending')  # e.g. pending, delivered, canceled
    comments = models.TextField(blank=True)
    
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderLineItem(models.Model):
    order = models.ForeignKey('orders_app.Order', null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'

# class Order(models.Model):
#     order_number = models.CharField(max_length=32, null=False, editable=False)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Associates order with a customer
#     full_name = models.CharField(max_length=50, null=False, blank=False)
#     email = models.EmailField(max_length=254, null=False, blank=False)
#     phone_number = models.CharField(max_length=20, null=False, blank=False)
#     country = CountryField(blank_label='Country *', null=False, blank=False)
#     postcode = models.CharField(max_length=20, null=True, blank=True)
#     town_or_city = models.CharField(max_length=40, null=False, blank=False)
#     street_address1 = models.CharField(max_length=80, null=False, blank=False)
#     street_address2 = models.CharField(max_length=80, null=True, blank=True)
#     county = models.CharField(max_length=80, null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)
#     delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
#     order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
#     grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
#     stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
#     status = models.CharField(max_length=20, default='pending')  # e.g., pending, delivered, canceled
#     comments = models.TextField(blank=True)

#     def _generate_order_number(self):
#         return uuid.uuid4().hex.upper()

#     def save(self, *args, **kwargs):
#         if not self.order_number:
#             self.order_number = self._generate_order_number()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.order_number

# class OrderLineItem(models.Model):
#     order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
#     product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE, related_name='order_products')  # ✅ Add unique related_name
#     quantity = models.IntegerField(null=False, blank=False, default=0)
#     lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

#     def save(self, *args, **kwargs):
#         self.lineitem_total = self.product.price * self.quantity
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.product.name} on order {self.order.order_number}'