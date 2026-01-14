from django.db import models
from django.contrib.auth.models import User
from tools.models import Tool

class Rental(models.Model):
    """
    Relational model linking a Borrower to a Tool.
    """
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='rental_history')
    start_date = models.DateField()
    end_date = models.DateField()
    is_returned = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tool.name} borrowed by {self.borrower.username}"