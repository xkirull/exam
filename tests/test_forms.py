import unittest
from tkinter import Tk
from views.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = MainWindow()
    
    def test_window_creation(self):
        self.assertIsNotNone(self.app.root)
        self.assertEqual(self.app.root.title(), "Заявки партнеров - Новые технологии")
    
    def tearDown(self):
        self.app.root.destroy()
