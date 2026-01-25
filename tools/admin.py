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
    Allows admin for borrowing records to update status and add notes.
    """
    list_display = ('tool', 'user', 'status', 'borrowed_date')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        # If the admin sets the status to 'returned',
        # automatically make the tool available
        if obj.status == 'returned':
            obj.tool.is_available = True
            obj.tool.save()
        # If the admin sets it to 'disputed' or
        # 'active', ensure it's unavailable
        elif obj.status in ['active', 'pending', 'disputed']:
            obj.tool.is_available = False
            obj.tool.save()

        super().save_model(request, obj, form, change)
