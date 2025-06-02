"""Утилиты для валидации данных"""
import re


class Validators:
    """Класс с методами валидации"""
    
    @staticmethod
    def validate_email(email):
        """Валидация email адреса"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Валидация телефона"""
        # Удаляем все символы кроме цифр
        digits = ''.join(filter(str.isdigit, phone))
        return len(digits) >= 10
    
    @staticmethod
    def validate_inn(inn):
        """Валидация ИНН"""
        return inn.isdigit() and len(inn) == 10
    
    @staticmethod
    def validate_rating(rating_str):
        """Валидация рейтинга"""
        try:
            rating = int(rating_str)
            return rating >= 0
        except ValueError:
            return False
