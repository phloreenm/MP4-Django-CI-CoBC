from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'delivery_cost', 'order_total', 'grand_total', 'stripe_pid')
    list_display = (
        'order_number',
        'date',
        'user',
        'order_total',
        'status')
    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)