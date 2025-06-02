"""Модель для работы с продукцией"""


class Product:
    """Класс для работы с продукцией"""
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_products(self):
        """Получение списка всей продукции"""
        query = """
            SELECT 
                p.id,
                p.product_name,
                p.article,
                p.min_cost_for_partner,
                pt.type_name as product_type
            FROM products p
            JOIN product_types pt ON p.product_type_id = pt.id
            ORDER BY p.product_name
        """
        return self.db.execute_query(query)
    
    def get_product_types(self):
        """Получение типов продукции с коэффициентами"""
        query = """
            SELECT id, type_name, coefficient
            FROM product_types
            ORDER BY type_name
        """
        return self.db.execute_query(query)
    
    def get_material_types(self):
        """Получение типов материалов с процентом брака"""
        query = """
            SELECT id, type_name, defect_percentage
            FROM material_types
            ORDER BY type_name
        """
        return self.db.execute_query(query)
    
    def create_product_type(self, type_name, coefficient):
        """Создание нового типа продукции"""
        query = """
            INSERT INTO product_types (type_name, coefficient)
            VALUES (%s, %s)
        """
        return self.db.execute_insert(query, (type_name, coefficient))
    
    def create_product(self, product_type_id, product_name, article, min_cost_for_partner):
        """Создание новой продукции"""
        query = """
            INSERT INTO products (product_type_id, product_name, article, min_cost_for_partner)
            VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_insert(query, (product_type_id, product_name, article, min_cost_for_partner))
    
    def check_article_exists(self, article):
        """Проверка существования артикула"""
        query = "SELECT COUNT(*) as count FROM products WHERE article = %s"
        result = self.db.execute_query(query, (article,))
        return result[0]['count'] > 0 if result else False
