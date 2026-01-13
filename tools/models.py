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
    Model representing an individual tool listed by a user.
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