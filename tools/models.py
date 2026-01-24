import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

class Category(models.Model):
    """
    Model representing tool categories for library organization.
    """
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    """
    Represents an individual tool owned by the Hub.
    """
    category = models.ForeignKey(
        'Category', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    # Note: Removed 'owner' to focus on B2C library model
    name = models.CharField(max_length=254)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    collection_date = models.DateField(null=True, blank=True)
    available_back_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Borrowing(models.Model):
    """
    Records the borrowing transaction between a User and a Hub Tool.
    """
    STATUS_CHOICES = [
        ('active', 'On Loan'),
        ('pending', 'Awaiting Review'),
        ('returned', 'Available'),
        ('disputed', 'Disputed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='borrows')
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    admin_notes = models.TextField(blank=True, null=True) # For feedback/damage notes
    user_notes = models.TextField(blank=True, null=True) # For user resolved comments

    def __str__(self):
        return f"{self.tool.name} - {self.status}"

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    username = os.getenv('ADMIN_USERNAME')
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PASSWORD')

    if username and email and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)