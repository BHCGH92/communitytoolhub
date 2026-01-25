from django.test import TestCase
from .models import Category, Tool
from django.contrib.auth.models import User


class TestToolModels(TestCase):
    """
    Test suite for Tool and Category models.
    Assesses data requirements and model functionality.
    """
    def setUp(self):
        # Create dependencies for the test
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Power Tools', friendly_name='Power Tools')

    def test_tool_string_method_returns_name(self):
        # Assess functionality of custom models
        tool = Tool.objects.create(
            name='Drill',
            category=self.category,
            price_per_day=10.00
        )
        self.assertEqual(str(tool), 'Drill')

    def test_category_friendly_name(self):
        # Verify custom logic for friendly names
        self.assertEqual(self.category.friendly_name, 'Power Tools')
