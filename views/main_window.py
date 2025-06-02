"""Главное окно приложения"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

from database.connection import DatabaseConnection
from models.partner_request import PartnerRequest
from views.request_card import RequestCard
from views.edit_window import EditWindow
from utils.styles import AppStyles


class MainWindow:
    """Главное окно приложения"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Заявки партнеров - Новые технологии")
        
        # Базовые размеры окна
        self.min_width = 900
        self.min_height = 600
        self.card_width = 850
        
        # Установка минимального размера окна
        self.root.minsize(self.min_width, self.min_height)
        
        # Центрирование окна на экране
        self.center_window()
        
        # Установка иконки приложения
        self.set_app_icon()
        
        # Подключение к базе данных
        self.db = DatabaseConnection()
        if not self.db.connect():
            self.root.destroy()
            return
        
        self.partner_request = PartnerRequest(self.db)
        
        # Применение стилей
        AppStyles.setup_styles(self.root)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка данных
        self.load_requests()
        
        # Обработка изменения размера окна
        self.root.bind('<Configure>', self.on_window_resize)
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - self.min_width) // 2
        y = (screen_height - self.min_height) // 2
        
        self.root.geometry(f'{self.min_width}x{self.min_height}+{x}+{y}')
    
    def on_window_resize(self, event):
        """Обработчик изменения размера окна"""
        if event.widget == self.root:
            max_width = self.card_width + 100
            if self.root.winfo_width() > max_width:
                self.root.geometry(f'{max_width}x{self.root.winfo_height()}')
    
    def set_app_icon(self):
        """Установка иконки приложения"""
        try:
            if os.path.exists('assets/icon.ico'):
                self.root.iconbitmap('assets/icon.ico')
            elif os.path.exists('assets/icon.png'):
                icon = Image.open('assets/icon.png')
                icon = icon.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(icon)
                self.root.iconphoto(True, photo)
        except:
            pass
    
    def create_widgets(self):
        """Создание виджетов главного окна"""
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=AppStyles.MAIN_BG)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок с логотипом
        header_frame = tk.Frame(main_container, bg=AppStyles.MAIN_BG)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Загрузка и отображение логотипа
        self.load_logo(header_frame)
        
        title_label = tk.Label(
            header_frame, 
            text="Система управления заявками партнеров",
            font=(AppStyles.MAIN_FONT, 20, 'bold'),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.ACCENT_COLOR
        )
        title_label.pack(side=tk.LEFT)
        
        # Панель инструментов
        toolbar_frame = tk.Frame(main_container, bg=AppStyles.SECONDARY_BG)
        toolbar_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        toolbar_label = tk.Label(
            toolbar_frame,
            text="Список заявок партнеров",
            font=(AppStyles.MAIN_FONT, 14, 'bold'),
            bg=AppStyles.SECONDARY_BG,
            fg=AppStyles.TEXT_COLOR
        )
        toolbar_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        # Кнопка добавления
        add_button = ttk.Button(
            toolbar_frame,
            text="Добавить заявку",
            style='Action.TButton',
            command=self.add_request
        )
        add_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Создание области с прокруткой для карточек
        self.create_scrollable_area(main_container)
    
    def load_logo(self, parent):
        """Загрузка и отображение логотипа компании"""
        try:
            logo_path = None
            for path in ['assets/logo.png', 'assets/logo.jpg', 'logo.png', 'logo.jpg']:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if logo_path:
                logo_image = Image.open(logo_path)
                logo_image.thumbnail((60, 60), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(parent, image=self.logo_photo, bg=AppStyles.MAIN_BG)
                logo_label.pack(side=tk.LEFT, padx=(0, 15))
            else:
                self.create_text_logo(parent)
        except:
            self.create_text_logo(parent)
    
    def create_text_logo(self, parent):
        """Создание текстового логотипа"""
        logo_frame = tk.Frame(parent, bg=AppStyles.ACCENT_COLOR, width=60, height=60)
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)
        
        logo_text = tk.Label(
            logo_frame,
            text="НТ",
            font=(AppStyles.MAIN_FONT, 24, 'bold'),
            bg=AppStyles.ACCENT_COLOR,
            fg=AppStyles.MAIN_BG
        )
        logo_text.place(relx=0.5, rely=0.5, anchor='center')
    
    def create_scrollable_area(self, parent):
        """Создание прокручиваемой области для карточек"""
        # Фрейм-контейнер
        container = tk.Frame(parent, bg=AppStyles.MAIN_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Canvas для прокрутки
        self.canvas = tk.Canvas(container, bg=AppStyles.MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=AppStyles.MAIN_BG)
        
        self.scrollable_frame.configure(width=self.card_width)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязка прокрутки колесом мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Обработчик прокрутки колесом мыши"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_requests(self):
        """Загрузка списка заявок"""
        # Очистка существующих карточек
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Получение данных
        requests = self.partner_request.get_all_requests_with_partners()
        
        if requests:
            for request in requests:
                # Создание карточки для каждой заявки
                card = RequestCard(
                    self.scrollable_frame,
                    request_id=request['request_id'],
                    partner_type=request['partner_type'],
                    company_name=request['company_name'],
                    address=request['legal_address'],
                    phone=request['phone'],
                    rating=request['rating'],
                    total_cost=float(request['total_cost']),
                    logo_data=request.get('logo'),
                    edit_callback=self.edit_request,
                    view_products_callback=self.view_products  # Добавляем callback
                )
                card.pack(fill=tk.X, padx=5, pady=5)
        
        # Обновляем область прокрутки
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def view_products(self, request_id, company_name):
        """Открытие окна просмотра продукции"""
        from views.products_window import ProductsWindow
        ProductsWindow(self.root, self.partner_request, request_id, company_name, self.load_requests)
    
    def edit_request(self, request_id):
        """Редактирование заявки"""
        # Получаем данные заявки
        request_data = self.partner_request.get_request_by_id(request_id)
        if not request_data:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные заявки")
            return
        
        # Открываем окно редактирования с callback для обновления
        EditWindow(self.root, self.partner_request, request_data, self.load_requests)
    
    def add_request(self):
        """Добавление новой заявки"""
        # Открываем окно добавления с callback для обновления
        EditWindow(self.root, self.partner_request, refresh_callback=self.load_requests)
    
    def run(self):
        """Запуск приложения"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти из приложения?"):
            self.db.disconnect()
            self.root.destroy()
