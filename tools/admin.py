from django.contrib import admin
from .models import Category, Tool, Borrowing

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for Category records.
    """
    list_display = (
        'friendly_name',
        'name',
    )

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for Tool records.
    """
    list_display = (
        'name',
        'category',
        'owner',
        'price_per_day',
        'is_available',
        'created_at',
    )
    # Adds a sidebar filter to help navigate larger data sets
    list_filter = ('category', 'is_available')
    # Adds a search bar for better User experience
    search_fields = ('name', 'description')

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for Borrowing records.
    """
    list_display = ('tool', 'user', 'borrowed_date', 'return_date', 'is_returned')
    list_filter = ('is_returned', 'borrowed_date')
    search_fields = ('user__username', 'tool__name')