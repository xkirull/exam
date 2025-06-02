"""Компонент карточки заявки"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.styles import AppStyles
import io


class RequestCard(tk.Frame):
    """Карточка заявки партнера"""
    def __init__(self, parent, request_id, partner_type, company_name, address, 
                 phone, rating, total_cost, logo_data=None, edit_callback=None, 
                 view_products_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.request_id = request_id
        self.edit_callback = edit_callback
        self.view_products_callback = view_products_callback
        self.company_name = company_name
        self.configure(bg=AppStyles.MAIN_BG, relief=tk.SOLID, borderwidth=1)
        
        # Список всех виджетов для установки обработчиков
        self.all_widgets = []
        
        # Создаем основной фрейм
        self.main_frame = tk.Frame(self, bg=AppStyles.MAIN_BG, cursor="hand2")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.all_widgets.append(self.main_frame)
        
        # При наведении меняем цвет границы
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Контейнер для логотипа и информации
        content_frame = tk.Frame(self.main_frame, bg=AppStyles.MAIN_BG)
        content_frame.pack(fill=tk.BOTH, expand=True)
        self.all_widgets.append(content_frame)
        
        # Логотип партнера (если есть)
        if logo_data:
            try:
                logo_image = Image.open(io.BytesIO(logo_data))
                logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(content_frame, image=logo_photo, bg=AppStyles.MAIN_BG, cursor="hand2")
                logo_label.image = logo_photo
                logo_label.pack(side=tk.LEFT, padx=(0, 10))
                self.all_widgets.append(logo_label)
            except:
                pass
        
        # Информационная часть
        info_frame = tk.Frame(content_frame, bg=AppStyles.MAIN_BG)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.all_widgets.append(info_frame)
        
        # Первая строка: Тип | Наименование партнера и Стоимость
        first_row = tk.Frame(info_frame, bg=AppStyles.MAIN_BG)
        first_row.pack(fill=tk.X)
        self.all_widgets.append(first_row)
        
        # Левая часть первой строки
        partner_info = tk.Label(
            first_row,
            text=f"{partner_type} | {company_name}",
            font=(AppStyles.MAIN_FONT, 14, 'bold'),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.TEXT_COLOR,
            anchor='w',
            cursor="hand2"
        )
        partner_info.pack(side=tk.LEFT)
        self.all_widgets.append(partner_info)
        
        # Правая часть первой строки - стоимость
        cost_label = tk.Label(
            first_row,
            text=f"{total_cost:.2f} руб.",
            font=(AppStyles.MAIN_FONT, 14, 'bold'),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.TEXT_COLOR,
            anchor='e',
            cursor="hand2"
        )
        cost_label.pack(side=tk.RIGHT)
        self.all_widgets.append(cost_label)
        
        # Остальные строки
        address_label = self._create_info_label(info_frame, address, pady=(5, 0))
        phone_label = self._create_info_label(info_frame, f"+{phone.replace(' ', ' ')}", pady=(2, 0))
        rating_label = self._create_info_label(info_frame, f"Рейтинг: {rating}", pady=(2, 0))
        
        # Панель с кнопками
        button_frame = tk.Frame(info_frame, bg=AppStyles.MAIN_BG)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Кнопка просмотра продукции
        products_button = ttk.Button(
            button_frame,
            text="Просмотр продукции",
            style='Action.TButton',
            command=self._view_products
        )
        products_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Устанавливаем обработчики клика на все виджеты
        self._setup_click_handlers()
    
    def _on_enter(self, event):
        """Обработчик наведения мыши"""
        self.configure(relief=tk.SOLID, borderwidth=2)
    
    def _on_leave(self, event):
        """Обработчик ухода мыши"""
        self.configure(relief=tk.SOLID, borderwidth=1)
    
    def _create_info_label(self, parent, text, **pack_options):
        """Создание информационной метки"""
        label = tk.Label(
            parent,
            text=text,
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.SECONDARY_TEXT,
            anchor='w',
            wraplength=700,
            cursor="hand2"
        )
        label.pack(fill=tk.X, **pack_options)
        self.all_widgets.append(label)
        return label
    
    def _setup_click_handlers(self):
        """Установка обработчиков клика на все элементы"""
        # Устанавливаем обработчик на саму карточку
        self.bind("<Button-1>", self.on_click)
        
        # Устанавливаем обработчик на все дочерние виджеты (кроме кнопок)
        for widget in self.all_widgets:
            widget.bind("<Button-1>", self.on_click)
            # Также привязываем события Enter/Leave для эффекта наведения
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
    
    def on_click(self, event):
        """Обработчик клика по карточке"""
        if self.edit_callback:
            self.edit_callback(self.request_id)
    
    def _view_products(self):
        """Просмотр продукции в заявке"""
        if self.view_products_callback:
            self.view_products_callback(self.request_id, self.company_name)
