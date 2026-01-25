from django.test import TestCase
from django.contrib.auth.models import User
from tools.models import Tool, Category
from .models import Rental
from datetime import date, timedelta


class RentalModelTest(TestCase):
    """Test suite for the Rental model relationships and logic"""
    def setUp(self):
        # Create a user, category, and tool for testing
        self.user = User.objects.create_user(username='borrower',
        password='password123')
        self.category = Category.objects.create(name='Power Tools')
        self.tool = Tool.objects.create(
            name='Hammer Drill',
            category=self.category,
            price_per_day=15.00,
            is_available=True
        )

    def test_rental_creation_and_relationship(self):
        """Verifies a rental can be linked to a user and tool"""
        rental = Rental.objects.create(
            borrower=self.user,
            tool=self.tool,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_price=30.00
        )
        self.assertEqual(rental.tool.name, 'Hammer Drill')
        self.assertEqual(rental.borrower.username, 'borrower')

    def test_rental_str_method(self):
        """Tests the professional representation of the object"""
        rental = Rental.objects.create(
            borrower=self.user,
            tool=self.tool,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            total_price=15.00
        )
        expected_str = f"Hammer Drill borrowed by borrower"
        self.assertEqual(str(rental), expected_str)
