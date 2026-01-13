from django.contrib import admin
from .models import Category, Tool

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
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