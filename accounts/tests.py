from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class TestProfileSignal(TestCase):
    def test_profile_is_created_when_user_is_created(self):
        """Verifies automated data handling through signals"""
        user = User.objects.create_user(username='newuser', password='password123')
        # Check if profile exists
        self.assertTrue(UserProfile.objects.filter(user=user).exists())