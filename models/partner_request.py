"""Модель для работы с заявками партнеров"""
from models.partner import Partner
from models.product import Product


class PartnerRequest:
    """Класс для работы с заявками партнеров"""
    def __init__(self, db_connection):
        self.db = db_connection
        self.partner = Partner(db_connection)
        self.product = Product(db_connection)
    
    def get_all_requests_with_partners(self):
        """Получение списка всех заявок с информацией о партнерах"""
        query = """
            SELECT 
                pr.id as request_id,
                pr.partner_id,
                pr.total_cost,
                pt.type_name as partner_type,
                p.company_name,
                p.legal_address,
                p.phone,
                p.rating,
                p.logo
            FROM partner_requests pr
            JOIN partners p ON pr.partner_id = p.id
            JOIN partner_types pt ON p.partner_type_id = pt.id
            ORDER BY pr.id DESC
        """
        return self.db.execute_query(query)
    
    def get_request_by_id(self, request_id):
        """Получение информации о конкретной заявке"""
        query = """
            SELECT 
                pr.id as request_id,
                pr.partner_id,
                pr.total_cost,
                pr.status,
                pt.id as partner_type_id,
                pt.type_name as partner_type,
                p.company_name,
                p.director_name,
                p.legal_address,
                p.phone,
                p.email,
                p.inn,
                p.rating
            FROM partner_requests pr
            JOIN partners p ON pr.partner_id = p.id
            JOIN partner_types pt ON p.partner_type_id = pt.id
            WHERE pr.id = %s
        """
        result = self.db.execute_query(query, (request_id,))
        return result[0] if result else None
    
    def create_request(self, partner_id):
        """Создание новой заявки"""
        query = """
            INSERT INTO partner_requests (partner_id, request_date, status, total_cost)
            VALUES (%s, NOW(), 'Новая', 0.00)
        """
        return self.db.execute_insert(query, (partner_id,))
    
    def update_request_partner(self, request_id, partner_id):
        """Обновление партнера в заявке"""
        query = "UPDATE partner_requests SET partner_id = %s WHERE id = %s"
        return self.db.execute_update(query, (partner_id, request_id))
    
    def get_request_products(self, request_id):
        """Получение списка продукции в заявке"""
        query = """
            SELECT 
                rp.id,
                rp.product_id,
                prod.product_name,
                prod.article,
                prod.min_cost_for_partner,
                rp.quantity,
                rp.cost_per_unit,
                ROUND(rp.quantity * rp.cost_per_unit, 2) as total_cost
            FROM request_products rp
            JOIN products prod ON rp.product_id = prod.id
            WHERE rp.request_id = %s
            ORDER BY prod.product_name
        """
        return self.db.execute_query(query, (request_id,))
    
    def add_product_to_request(self, request_id, product_id, quantity):
        """Добавление продукции в заявку"""
        # Получаем минимальную стоимость продукта
        query = "SELECT min_cost_for_partner FROM products WHERE id = %s"
        result = self.db.execute_query(query, (product_id,))
        if not result:
            return False
        
        cost_per_unit = float(result[0]['min_cost_for_partner'])
        
        # Добавляем продукт в заявку
        query = """
            INSERT INTO request_products (request_id, product_id, quantity, cost_per_unit)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = %s, cost_per_unit = %s
        """
        params = (request_id, product_id, quantity, cost_per_unit, quantity, cost_per_unit)
        success = self.db.execute_update(query, params)
        
        if success:
            # Обновляем общую стоимость заявки
            self.update_request_total(request_id)
        
        return success
    
    def remove_product_from_request(self, request_id, product_id):
        """Удаление продукции из заявки"""
        query = "DELETE FROM request_products WHERE request_id = %s AND product_id = %s"
        success = self.db.execute_update(query, (request_id, product_id))
        
        if success:
            # Обновляем общую стоимость заявки
            self.update_request_total(request_id)
        
        return success
    
    def update_request_total(self, request_id):
        """Обновление общей стоимости заявки"""
        query = """
            UPDATE partner_requests 
            SET total_cost = (
                SELECT COALESCE(SUM(quantity * cost_per_unit), 0)
                FROM request_products
                WHERE request_id = %s
            )
            WHERE id = %s
        """
        return self.db.execute_update(query, (request_id, request_id))
