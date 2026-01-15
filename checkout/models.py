from django.db import models
from django.contrib.auth.models import User
from tools.models import Tool

class Order(models.Model):
    """
    Model for storing payment and transaction details.
    Demonstrates integration of external payment logic.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    order_number = models.CharField(max_length=32, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_pid = models.CharField(max_length=254, default='')

    def __str__(self):
        return self.order_number