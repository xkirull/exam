# utils/styles.py
"""Стили для приложения"""
from tkinter import ttk


class AppStyles:
    """Класс для настройки стилей приложения"""
    
    # Цвета
    MAIN_BG = '#FFFFFF'
    SECONDARY_BG = '#BBDCFA'
    ACCENT_COLOR = '#0C4882'
    TEXT_COLOR = '#000000'
    SECONDARY_TEXT = '#666666'
    
    # Шрифты
    MAIN_FONT = 'Bahnschrift Light SemiCondensed'
    
    @staticmethod
    def setup_styles(root):
        """Настройка стилей согласно руководству"""
        root.configure(bg=AppStyles.MAIN_BG)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Стиль для кнопок
        style.configure(
            'Action.TButton',
            background=AppStyles.ACCENT_COLOR,
            foreground=AppStyles.MAIN_BG,
            font=(AppStyles.MAIN_FONT, 12),
            borderwidth=0,
            focuscolor='none'
        )
        style.map(
            'Action.TButton',
            background=[('active', AppStyles.SECONDARY_BG)]
        )
        
        # Стиль для полей ввода
        style.configure(
            'Custom.TEntry',
            fieldbackground=AppStyles.MAIN_BG,
            borderwidth=1,
            relief='solid',
            font=(AppStyles.MAIN_FONT, 11)
        )
        
        # Стиль для Combobox
        style.configure(
            'Custom.TCombobox',
            fieldbackground=AppStyles.MAIN_BG,
            borderwidth=1,
            relief='solid',
            font=(AppStyles.MAIN_FONT, 11)
        )
