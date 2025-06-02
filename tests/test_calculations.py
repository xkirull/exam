import unittest
from utils.calculations import calculate_order_cost
from utils.material_calculator import calculate_material_amount

class TestCalculations(unittest.TestCase):
    def test_order_cost_calculation(self):
        products = [
            {'quantity': 10, 'min_cost_for_partner': 100.50},
            {'quantity': 5, 'min_cost_for_partner': 200.00}
        ]
        result = calculate_order_cost(products)
        self.assertEqual(result, 2005.00)
    
    def test_material_calculation_valid(self):
        result = calculate_material_amount(1, 1, 100, 20, 2.5, 3.0)
        self.assertEqual(result, 901)  # Ожидаемый результат
    
    def test_material_calculation_invalid_type(self):
        result = calculate_material_amount(999, 1, 100, 20, 2.5, 3.0)
        self.assertEqual(result, -1)
