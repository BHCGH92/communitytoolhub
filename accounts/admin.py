from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'town_or_city', 'phone_number')
    search_fields = ('user__username', 'town_or_city')