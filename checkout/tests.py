from django.test import TestCase
from .models import Order


class TestOrderModel(TestCase):
    def test_order_string_method(self):
        """Tests that the order number is used as the string representation"""
        order = Order.objects.create(
            full_name="Test User",
            email="test@test.com",
            order_number="12345",
            order_total=15.00
        )
        self.assertEqual(str(order), "12345")
