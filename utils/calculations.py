"""Утилиты для расчетов"""
from decimal import Decimal, ROUND_HALF_UP


def calculate_order_cost(products_list):
    """
    Расчет стоимости заявки на основе списка продукции
    
    Args:
        products_list: список словарей с информацией о продукции
                      [{'quantity': int, 'min_cost_for_partner': float}, ...]
    
    Returns:
        float: общая стоимость заявки с точностью до сотых
    """
    total_cost = Decimal('0.00')
    
    for product in products_list:
        quantity = Decimal(str(product['quantity']))
        price = Decimal(str(product['min_cost_for_partner']))
        
        # Расчет стоимости для каждой позиции
        product_cost = quantity * price
        total_cost += product_cost
    
    # Округление до сотых
    total_cost = total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Проверка на отрицательное значение
    if total_cost < 0:
        total_cost = Decimal('0.00')
    
    return float(total_cost)
