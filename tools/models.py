import os
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Model representing tool categories (For Example Gardening, Power Tools etc.).
    Will help organize the library for better UX.
    """
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Tool(models.Model):
    """
    Represents an individual tool listed by a user.
    Demonstrates CRUD and data modelling techniques.
    """
    category = models.ForeignKey(
        'Category', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='tools'
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Borrowing(models.Model):
    """
    Records the borrowing of a tool by a user, including dates and status.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='borrows')
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.tool.name}"

# Automatically create a superuser after migrations
@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    # Pull values from environment variables instead of hard-coding them
    username = os.getenv('ADMIN_USERNAME')
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PASSWORD')

    # Only run if all variables are set and user doesn't exist yet
    if username and email and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print(f"Superuser '{username}' created automatically.")