from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date', 'stripe_pid')
    list_display = ('order_number', 'date', 'full_name', 'order_total')
    ordering = ('-date',)