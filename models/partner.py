"""Модель для работы с партнерами"""


class Partner:
    """Класс для работы с партнерами"""
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_partners(self):
        """Получение списка всех партнеров"""
        query = """
            SELECT p.id, p.company_name, pt.type_name
            FROM partners p
            JOIN partner_types pt ON p.partner_type_id = pt.id
            ORDER BY p.company_name
        """
        return self.db.execute_query(query)
    
    def get_partner_types(self):
        """Получение типов партнеров"""
        query = "SELECT id, type_name FROM partner_types ORDER BY type_name"
        return self.db.execute_query(query)
    
    def update_partner(self, partner_id, partner_type_id, company_name, director_name, 
                      email, phone, legal_address, inn, rating):
        """Обновление данных партнера"""
        query = """
            UPDATE partners 
            SET partner_type_id = %s, company_name = %s, director_name = %s,
                email = %s, phone = %s, legal_address = %s, inn = %s, rating = %s
            WHERE id = %s
        """
        params = (partner_type_id, company_name, director_name, email, phone, 
                 legal_address, inn, rating, partner_id)
        return self.db.execute_update(query, params)
    
    def create_partner(self, partner_type_id, company_name, director_name, 
                      email, phone, legal_address, inn, rating):
        """Создание нового партнера"""
        query = """
            INSERT INTO partners (partner_type_id, company_name, director_name, 
                                email, phone, legal_address, inn, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (partner_type_id, company_name, director_name, email, phone, 
                 legal_address, inn, rating)
        return self.db.execute_insert(query, params)
