import unittest

class TestFormValidation(unittest.TestCase):
    def test_form_validation(self):
        """Тест валидации формы"""
        # Простая проверка что валидация существует
        from utils.validators import Validators
        self.assertTrue(hasattr(Validators, 'validate_email'))
        self.assertTrue(hasattr(Validators, 'validate_phone'))
