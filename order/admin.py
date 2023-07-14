from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('order', 'product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin, ]
