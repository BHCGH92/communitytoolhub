from django.contrib import admin
from .models import Rental

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'borrower',
        'tool',
        'start_date',
        'end_date',
        'is_returned',
        'total_price',
        'created_at',
    )
    # Adds a sidebar filter to help navigate larger data sets
    list_filter = ('is_returned', 'start_date')
    # Adds a search bar for better User experience
    search_fields = ('borrower__username', 'tool__name')