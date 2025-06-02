import unittest
from utils.calculations import calculate_order_cost

class TestCalculations(unittest.TestCase):
    def test_order_cost_calculation(self):
        """Тест расчета стоимости заказа"""
        products = [
            {'quantity': 10, 'min_cost_for_partner': 100.50},
            {'quantity': 5, 'min_cost_for_partner': 200.00}
        ]
        result = calculate_order_cost(products)
        self.assertEqual(result, 2005.00)
    
    def test_order_cost_empty(self):
        """Тест пустого списка"""
        products = []
        result = calculate_order_cost(products)
        self.assertEqual(result, 0.00)
