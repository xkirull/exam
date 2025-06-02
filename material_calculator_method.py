"""
Метод расчета количества материала для производства продукции
"""

def calculate_material_amount(product_type_id, material_type_id, required_quantity, 
                            stock_quantity, param1, param2):
    """
    Расчет количества необходимого материала для производства продукции
    
    Args:
        product_type_id (int): идентификатор типа продукции
        material_type_id (int): идентификатор типа материала
        required_quantity (int): требуемое количество продукции
        stock_quantity (int): количество продукции на складе
        param1 (float): первый параметр продукции (положительное число)
        param2 (float): второй параметр продукции (положительное число)
    
    Returns:
        int: количество необходимого материала или -1 при ошибке
    """
    try:
        # Валидация входных данных
        if not all(isinstance(x, int) for x in [product_type_id, material_type_id, 
                                                required_quantity, stock_quantity]):
            return -1
            
        if not all(isinstance(x, (int, float)) for x in [param1, param2]):
            return -1
            
        if any(x < 0 for x in [required_quantity, stock_quantity]):
            return -1
            
        if param1 <= 0 or param2 <= 0:
            return -1
        
        # Словарь коэффициентов типов продукции
        product_coefficients = {
            1: 1.5,   # Древесно-плитные материалы
            2: 3.5,   # Декоративные панели
            3: 5.25,  # Плитка
            4: 4.5,   # Фасадные материалы
            5: 2.17   # Напольные покрытия
        }
        
        # Словарь процентов брака материалов
        material_defects = {
            1: 0.002,   # Тип материала 1
            2: 0.005,   # Тип материала 2
            3: 0.003,   # Тип материала 3
            4: 0.0015,  # Тип материала 4
            5: 0.0018   # Тип материала 5
        }
        
        # Проверка существования типов
        if product_type_id not in product_coefficients:
            return -1
        if material_type_id not in material_defects:
            return -1
        
        # Получаем коэффициенты
        product_coefficient = product_coefficients[product_type_id]
        defect_percentage = material_defects[material_type_id]
        
        # Вычисляем количество продукции для производства
        quantity_to_produce = max(0, required_quantity - stock_quantity)
        
        if quantity_to_produce == 0:
            return 0
        
        # Вычисляем количество материала на единицу продукции
        material_per_unit = param1 * param2 * product_coefficient
        
        # Вычисляем базовое количество материала
        base_material = material_per_unit * quantity_to_produce
        
        # Учитываем процент брака
        material_with_defect = base_material / (1 - defect_percentage)
        
        # Округляем вверх до целого числа
        import math
        result = math.ceil(material_with_defect)
        
        return result
        
    except:
        return -1
