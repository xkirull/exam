"""Модуль для расчета необходимого количества материалов"""
from decimal import Decimal, ROUND_UP


class MaterialCalculator:
    """Класс для расчета материалов"""
    
    @staticmethod
    def calculate_material_amount(product_type_id, material_type_id, required_quantity, 
                                 stock_quantity, param1, param2, db_connection):
        """
        Расчет количества необходимого материала
        
        Args:
            product_type_id: идентификатор типа продукции
            material_type_id: идентификатор типа материала
            required_quantity: требуемое количество продукции
            stock_quantity: количество продукции на складе
            param1: первый параметр продукции
            param2: второй параметр продукции
            db_connection: подключение к БД для получения коэффициентов
            
        Returns:
            int: количество необходимого материала или -1 при ошибке
        """
        try:
            # Валидация входных данных
            if any(x < 0 for x in [required_quantity, stock_quantity]):
                return -1
            
            if param1 <= 0 or param2 <= 0:
                return -1
            
            # Получаем коэффициент типа продукции
            query = "SELECT coefficient FROM product_types WHERE id = %s"
            result = db_connection.execute_query(query, (product_type_id,))
            if not result:
                return -1
            product_coefficient = Decimal(str(result[0]['coefficient']))
            
            # Получаем процент брака материала
            query = "SELECT defect_percentage FROM material_types WHERE id = %s"
            result = db_connection.execute_query(query, (material_type_id,))
            if not result:
                return -1
            defect_percentage = Decimal(str(result[0]['defect_percentage']))
            
            # Вычисляем количество продукции для производства (с учетом склада)
            quantity_to_produce = max(0, required_quantity - stock_quantity)
            
            if quantity_to_produce == 0:
                return 0
            
            # Вычисляем количество материала на единицу продукции
            param1_decimal = Decimal(str(param1))
            param2_decimal = Decimal(str(param2))
            material_per_unit = param1_decimal * param2_decimal * product_coefficient
            
            # Вычисляем базовое количество материала
            base_material = material_per_unit * Decimal(str(quantity_to_produce))
            
            # Учитываем процент брака (увеличиваем количество)
            # Формула: необходимое_количество = базовое_количество / (1 - процент_брака)
            material_with_defect = base_material / (Decimal('1') - defect_percentage)
            
            # Округляем вверх до целого числа
            result = int(material_with_defect.quantize(Decimal('1'), rounding=ROUND_UP))
            
            return result
            
        except Exception as e:
            # В случае любой ошибки возвращаем -1
            return -1


def calculate_material_amount(product_type_id, material_type_id, required_quantity, 
                            stock_quantity, param1, param2, db_connection):
    """
    Функция-обертка для расчета материалов
    
    Метод рассчитывает целое количество материала, необходимого для производства 
    требуемого количества продукции, учитывая наличие продукции на складе и 
    возможный брак материала.
    """
    return MaterialCalculator.calculate_material_amount(
        product_type_id, material_type_id, required_quantity, 
        stock_quantity, param1, param2, db_connection
    )
