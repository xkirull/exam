import unittest
from utils.validators import Validators

class TestValidators(unittest.TestCase):
    def test_email_valid(self):
        """Тест валидного email"""
        self.assertTrue(Validators.validate_email('test@example.com'))
    
    def test_email_invalid(self):
        """Тест невалидного email"""
        self.assertFalse(Validators.validate_email('test'))
    
    def test_phone_valid(self):
        """Тест валидного телефона"""
        self.assertTrue(Validators.validate_phone('+74951234567'))
    
    def test_inn_valid(self):
        """Тест валидного ИНН"""
        self.assertTrue(Validators.validate_inn('1234567890'))
    
    def test_rating_valid(self):
        """Тест валидного рейтинга"""
        self.assertTrue(Validators.validate_rating('5'))
