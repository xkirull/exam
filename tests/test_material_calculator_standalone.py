import unittest

def calculate_material_amount(product_type_id, material_type_id, required_quantity, 
                            stock_quantity, param1, param2):
    """Автономная версия расчета материалов для тестирования"""
    # Словари с данными из БД
    product_coefficients = {1: 1.5, 2: 3.5, 3: 5.25, 4: 4.5, 5: 2.17}
    material_defects = {1: 0.002, 2: 0.005, 3: 0.003, 4: 0.0015, 5: 0.0018}
    
    # Валидация
    if product_type_id not in product_coefficients:
        return -1
    if material_type_id not in material_defects:
        return -1
    if any(x < 0 for x in [required_quantity, stock_quantity]):
        return -1
    if param1 <= 0 or param2 <= 0:
        return -1
    
    # Расчет
    quantity_to_produce = max(0, required_quantity - stock_quantity)
    if quantity_to_produce == 0:
        return 0
    
    material_per_unit = param1 * param2 * product_coefficients[product_type_id]
    base_material = material_per_unit * quantity_to_produce
    material_with_defect = base_material / (1 - material_defects[material_type_id])
    
    import math
    return math.ceil(material_with_defect)

class TestMaterialCalculator(unittest.TestCase):
    def test_valid_calculation(self):
        """Тест корректного расчета"""
        result = calculate_material_amount(1, 1, 100, 20, 2.5, 3.0)
        self.assertEqual(result, 902)
    
    def test_invalid_type(self):
        """Тест с несуществующим типом"""
        result = calculate_material_amount(999, 1, 100, 20, 2.5, 3.0)
        self.assertEqual(result, -1)
