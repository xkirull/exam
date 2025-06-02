"""Окно просмотра и редактирования продукции в заявке"""
import tkinter as tk
from tkinter import ttk, messagebox
from utils.styles import AppStyles
from utils.validators import Validators


class ProductsWindow:
    """Окно для работы с продукцией в заявке"""
    
    def __init__(self, parent, partner_request, request_id, partner_name, refresh_callback=None):
        self.parent = parent
        self.partner_request = partner_request
        self.request_id = request_id
        self.partner_name = partner_name
        self.refresh_callback = refresh_callback
        
        # Создание окна
        self.window = tk.Toplevel(parent)
        self.window.title(f"Продукция в заявке №{request_id} - Новые технологии")
        self.window.geometry("900x600")
        self.window.configure(bg=AppStyles.MAIN_BG)
        
        # Делаем окно модальным
        self.window.transient(parent)
        self.window.grab_set()
        
        # Центрируем окно
        self._center_window()
        
        # Создаем интерфейс
        self._create_widgets()
        
        # Загружаем данные
        self.load_products()
    
    def _center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 900) // 2
        y = (self.window.winfo_screenheight() - 600) // 2
        self.window.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Создание виджетов окна"""
        # Заголовок
        header_frame = tk.Frame(self.window, bg=AppStyles.MAIN_BG)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        header_label = tk.Label(
            header_frame,
            text=f"Продукция для партнера: {self.partner_name}",
            font=(AppStyles.MAIN_FONT, 18, 'bold'),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.ACCENT_COLOR
        )
        header_label.pack(side=tk.LEFT)
        
        # Кнопка закрытия
        close_button = ttk.Button(
            header_frame,
            text="Закрыть",
            style='Action.TButton',
            command=self._on_close
        )
        close_button.pack(side=tk.RIGHT)
        
        # Панель инструментов
        toolbar_frame = tk.Frame(self.window, bg=AppStyles.SECONDARY_BG)
        toolbar_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        toolbar_label = tk.Label(
            toolbar_frame,
            text="Список продукции в заявке",
            font=(AppStyles.MAIN_FONT, 14, 'bold'),
            bg=AppStyles.SECONDARY_BG,
            fg=AppStyles.TEXT_COLOR
        )
        toolbar_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        # Кнопка добавления продукции
        add_button = ttk.Button(
            toolbar_frame,
            text="Добавить продукцию",
            style='Action.TButton',
            command=self._add_product
        )
        add_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Кнопка удаления продукции
        self.remove_button = ttk.Button(
            toolbar_frame,
            text="Удалить выбранное",
            style='Action.TButton',
            command=self._remove_product,
            state='disabled'
        )
        self.remove_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Таблица продукции
        self._create_products_table()
        
        # Панель с итоговой суммой
        self._create_total_panel()
    
    def _create_products_table(self):
        """Создание таблицы продукции"""
        # Фрейм для таблицы
        table_frame = tk.Frame(self.window, bg=AppStyles.MAIN_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Создание Treeview
        columns = ('Наименование', 'Артикул', 'Количество', 'Цена за ед.', 'Сумма')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Настройка колонок
        self.tree.column('Наименование', width=350)
        self.tree.column('Артикул', width=100, anchor='center')
        self.tree.column('Количество', width=100, anchor='center')
        self.tree.column('Цена за ед.', width=120, anchor='e')
        self.tree.column('Сумма', width=120, anchor='e')
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Обработчик выбора
        self.tree.bind('<<TreeviewSelect>>', self._on_selection_change)
        
        # Стиль для таблицы
        style = ttk.Style()
        style.configure(
            'Treeview',
            background=AppStyles.MAIN_BG,
            fieldbackground=AppStyles.MAIN_BG,
            font=(AppStyles.MAIN_FONT, 11)
        )
        style.configure(
            'Treeview.Heading',
            background=AppStyles.SECONDARY_BG,
            font=(AppStyles.MAIN_FONT, 12, 'bold')
        )
    
    def _create_total_panel(self):
        """Создание панели с итоговой суммой"""
        total_frame = tk.Frame(self.window, bg=AppStyles.SECONDARY_BG)
        total_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.total_label = tk.Label(
            total_frame,
            text="Итоговая стоимость заявки: 0.00 руб.",
            font=(AppStyles.MAIN_FONT, 14, 'bold'),
            bg=AppStyles.SECONDARY_BG
        )
        self.total_label.pack(padx=10, pady=10)
    
    def load_products(self):
        """Загрузка продукции в заявке"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение данных
        products = self.partner_request.get_request_products(self.request_id)
        total_sum = 0
        
        if products:
            for product in products:
                # Добавляем продукт в таблицу с сохранением ID
                item = self.tree.insert(
                    '',
                    'end',
                    values=(
                        product['product_name'],
                        product['article'],
                        product['quantity'],
                        f"{product['cost_per_unit']:.2f} руб.",
                        f"{product['total_cost']:.2f} руб."
                    ),
                    tags=(product['product_id'],)  # Сохраняем ID продукта
                )
                total_sum += float(product['total_cost'])
        
        # Обновляем итоговую сумму
        self.total_label.config(text=f"Итоговая стоимость заявки: {total_sum:.2f} руб.")
    
    def _on_selection_change(self, event):
        """Обработчик изменения выбора в таблице"""
        selection = self.tree.selection()
        if selection:
            self.remove_button.config(state='normal')
        else:
            self.remove_button.config(state='disabled')
    
    def _add_product(self):
        """Добавление продукции в заявку"""
        # Создаем окно выбора продукции
        AddProductDialog(self.window, self.partner_request, self.request_id, self.load_products)
    
    def _remove_product(self):
        """Удаление выбранной продукции"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Подтверждение удаления
        if not messagebox.askyesno("Подтверждение", 
                                  "Вы уверены, что хотите удалить выбранную продукцию?",
                                  parent=self.window):
            return
        
        # Получаем ID продукта из тегов
        item = self.tree.item(selection[0])
        if item['tags']:
            product_id = item['tags'][0]
            
            # Удаляем продукт из заявки
            if self.partner_request.remove_product_from_request(self.request_id, product_id):
                messagebox.showinfo("Успех", "Продукция успешно удалена", parent=self.window)
                self.load_products()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить продукцию", parent=self.window)
    
    def _on_close(self):
        """Закрытие окна"""
        self.window.destroy()
        # Обновляем главное окно
        if self.refresh_callback:
            self.refresh_callback()


class AddProductDialog:
    """Диалог добавления продукции в заявку"""
    
    def __init__(self, parent, partner_request, request_id, refresh_callback):
        self.parent = parent
        self.partner_request = partner_request
        self.request_id = request_id
        self.refresh_callback = refresh_callback
        
        # Создание диалога
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавление продукции")
        self.dialog.geometry("600x400")
        self.dialog.configure(bg=AppStyles.MAIN_BG)
        
        # Делаем окно модальным
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно
        self._center_dialog()
        
        # Создаем интерфейс
        self._create_widgets()
    
    def _center_dialog(self):
        """Центрирование диалога"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - 600) // 2
        y = (self.dialog.winfo_screenheight() - 400) // 2
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Создание виджетов диалога"""
        # Заголовок
        header_label = tk.Label(
            self.dialog,
            text="Выберите продукцию для добавления",
            font=(AppStyles.MAIN_FONT, 14, 'bold'),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.ACCENT_COLOR
        )
        header_label.pack(pady=(20, 10))
        
        # Notebook для вкладок
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Вкладка существующей продукции
        existing_frame = tk.Frame(notebook, bg=AppStyles.MAIN_BG)
        notebook.add(existing_frame, text="Существующая продукция")
        self._create_existing_product_tab(existing_frame)
        
        # Вкладка новой продукции
        new_frame = tk.Frame(notebook, bg=AppStyles.MAIN_BG)
        notebook.add(new_frame, text="Новая продукция")
        self._create_new_product_tab(new_frame)
    
    def _create_existing_product_tab(self, parent):
        """Создание вкладки существующей продукции"""
        # Форма
        form_frame = tk.Frame(parent, bg=AppStyles.MAIN_BG)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Выбор продукции
        tk.Label(
            form_frame,
            text="Продукция:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        # Получаем список продукции
        products = self.partner_request.product.get_all_products()
        self.products_dict = {f"{p['product_name']} ({p['article']})": p for p in products}
        
        self.product_var = tk.StringVar()
        product_combo = ttk.Combobox(
            form_frame,
            textvariable=self.product_var,
            values=list(self.products_dict.keys()),
            style='Custom.TCombobox',
            state='readonly',
            width=40
        )
        product_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        product_combo.bind('<<ComboboxSelected>>', self._on_product_select)
        
        # Количество
        tk.Label(
            form_frame,
            text="Количество:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(
            form_frame,
            textvariable=self.quantity_var,
            style='Custom.TEntry'
        )
        quantity_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Информация о цене
        self.price_label = tk.Label(
            form_frame,
            text="",
            font=(AppStyles.MAIN_FONT, 11),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.SECONDARY_TEXT
        )
        self.price_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Кнопки
        button_frame = tk.Frame(parent, bg=AppStyles.MAIN_BG)
        button_frame.pack(pady=(0, 20))
        
        add_button = ttk.Button(
            button_frame,
            text="Добавить",
            style='Action.TButton',
            command=self._add_existing
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame,
            text="Отмена",
            style='Action.TButton',
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def _create_new_product_tab(self, parent):
        """Создание вкладки новой продукции"""
        # Форма
        form_frame = tk.Frame(parent, bg=AppStyles.MAIN_BG)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Тип продукции
        tk.Label(
            form_frame,
            text="Тип продукции:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        type_frame = tk.Frame(form_frame, bg=AppStyles.MAIN_BG)
        type_frame.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Получаем типы продукции
        product_types = self.partner_request.product.get_product_types()
        self.product_types_dict = {pt['type_name']: pt for pt in product_types}
        
        self.new_type_var = tk.StringVar()
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.new_type_var,
            values=list(self.product_types_dict.keys()),
            style='Custom.TCombobox',
            state='readonly'
        )
        type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Кнопка добавления нового типа
        new_type_button = ttk.Button(
            type_frame,
            text="Новый тип",
            style='Action.TButton',
            command=self._create_new_type
        )
        new_type_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Наименование продукции
        tk.Label(
            form_frame,
            text="Наименование:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.new_name_var = tk.StringVar()
        name_entry = ttk.Entry(
            form_frame,
            textvariable=self.new_name_var,
            style='Custom.TEntry'
        )
        name_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Артикул
        tk.Label(
            form_frame,
            text="Артикул:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        self.new_article_var = tk.StringVar()
        article_entry = ttk.Entry(
            form_frame,
            textvariable=self.new_article_var,
            style='Custom.TEntry'
        )
        article_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Минимальная стоимость
        tk.Label(
            form_frame,
            text="Мин. стоимость:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=3, column=0, sticky='w', pady=5)
        
        self.new_cost_var = tk.StringVar()
        cost_entry = ttk.Entry(
            form_frame,
            textvariable=self.new_cost_var,
            style='Custom.TEntry'
        )
        cost_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Количество
        tk.Label(
            form_frame,
            text="Количество:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=4, column=0, sticky='w', pady=5)
        
        self.new_quantity_var = tk.StringVar(value="1")
        new_quantity_entry = ttk.Entry(
            form_frame,
            textvariable=self.new_quantity_var,
            style='Custom.TEntry'
        )
        new_quantity_entry.grid(row=4, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Кнопки
        button_frame = tk.Frame(parent, bg=AppStyles.MAIN_BG)
        button_frame.pack(pady=(0, 20))
        
        create_button = ttk.Button(
            button_frame,
            text="Создать и добавить",
            style='Action.TButton',
            command=self._create_and_add
        )
        create_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame,
            text="Отмена",
            style='Action.TButton',
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def _create_new_type(self):
        """Создание нового типа продукции"""
        # Диалог для нового типа
        type_dialog = tk.Toplevel(self.dialog)
        type_dialog.title("Новый тип продукции")
        type_dialog.geometry("400x200")
        type_dialog.configure(bg=AppStyles.MAIN_BG)
        type_dialog.transient(self.dialog)
        type_dialog.grab_set()
        
        # Центрируем
        type_dialog.update_idletasks()
        x = (type_dialog.winfo_screenwidth() - 400) // 2
        y = (type_dialog.winfo_screenheight() - 200) // 2
        type_dialog.geometry(f"+{x}+{y}")
        
        # Форма
        form_frame = tk.Frame(type_dialog, bg=AppStyles.MAIN_BG)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Название типа
        tk.Label(
            form_frame,
            text="Название типа:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        type_name_var = tk.StringVar()
        type_name_entry = ttk.Entry(
            form_frame,
            textvariable=type_name_var,
            style='Custom.TEntry'
        )
        type_name_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Коэффициент
        tk.Label(
            form_frame,
            text="Коэффициент:",
            font=(AppStyles.MAIN_FONT, 12),
            bg=AppStyles.MAIN_BG
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        coefficient_var = tk.StringVar(value="1.0")
        coefficient_entry = ttk.Entry(
            form_frame,
            textvariable=coefficient_var,
            style='Custom.TEntry'
        )
        coefficient_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Кнопки
        def save_type():
            # Валидация
            if not type_name_var.get().strip():
                messagebox.showerror("Ошибка", "Введите название типа", parent=type_dialog)
                return
            
            try:
                coefficient = float(coefficient_var.get())
                if coefficient <= 0:
                    messagebox.showerror("Ошибка", "Коэффициент должен быть положительным числом", parent=type_dialog)
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Коэффициент должен быть числом", parent=type_dialog)
                return
            
            # Создаем новый тип
            type_id = self.partner_request.product.create_product_type(
                type_name_var.get().strip(),
                coefficient
            )
            
            if type_id:
                messagebox.showinfo("Успех", "Тип продукции успешно создан", parent=type_dialog)
                
                # Обновляем список типов
                product_types = self.partner_request.product.get_product_types()
                self.product_types_dict = {pt['type_name']: pt for pt in product_types}
                
                # Обновляем комбобокс
                type_combo = type_dialog.master.nametowidget(type_combo_name)
                type_combo['values'] = list(self.product_types_dict.keys())
                self.new_type_var.set(type_name_var.get().strip())
                
                type_dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать тип продукции", parent=type_dialog)
        
        button_frame = tk.Frame(type_dialog, bg=AppStyles.MAIN_BG)
        button_frame.pack(pady=10)
        
        save_button = ttk.Button(
            button_frame,
            text="Сохранить",
            style='Action.TButton',
            command=save_type
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame,
            text="Отмена",
            style='Action.TButton',
            command=type_dialog.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Сохраняем имя комбобокса для обновления
        for widget in form_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox):
                        type_combo_name = str(child)
                        break
    
    def _on_product_select(self, event):
        """Обработчик выбора продукции"""
        if self.product_var.get():
            product = self.products_dict[self.product_var.get()]
            self.price_label.config(
                text=f"Минимальная стоимость для партнера: {product['min_cost_for_partner']:.2f} руб."
            )
    
    def _add_existing(self):
        """Добавление существующей продукции"""
        # Валидация
        if not self.product_var.get():
            messagebox.showerror("Ошибка", "Выберите продукцию", parent=self.dialog)
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Ошибка", "Количество должно быть положительным числом", parent=self.dialog)
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом", parent=self.dialog)
            return
        
        # Получаем выбранный продукт
        product = self.products_dict[self.product_var.get()]
        
        # Добавляем продукт в заявку
        if self.partner_request.add_product_to_request(self.request_id, product['id'], quantity):
            messagebox.showinfo("Успех", "Продукция успешно добавлена", parent=self.dialog)
            self.dialog.destroy()
            # Обновляем список продукции
            if self.refresh_callback:
                self.refresh_callback()
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить продукцию", parent=self.dialog)
    
    def _create_and_add(self):
        """Создание новой продукции и добавление в заявку"""
        # Валидация
        errors = []
        
        if not self.new_type_var.get():
            errors.append("Выберите тип продукции")
        
        if not self.new_name_var.get().strip():
            errors.append("Введите наименование продукции")
        
        if not self.new_article_var.get().strip():
            errors.append("Введите артикул")
        
        # Проверка уникальности артикула
        if self.new_article_var.get().strip():
            if self.partner_request.product.check_article_exists(self.new_article_var.get().strip()):
                errors.append("Продукция с таким артикулом уже существует")
        
        try:
            cost = float(self.new_cost_var.get())
            if cost <= 0:
                errors.append("Минимальная стоимость должна быть положительным числом")
        except ValueError:
            errors.append("Минимальная стоимость должна быть числом")
        
        try:
            quantity = int(self.new_quantity_var.get())
            if quantity <= 0:
                errors.append("Количество должно быть положительным числом")
        except ValueError:
            errors.append("Количество должно быть целым числом")
        
        if errors:
            error_message = "Обнаружены следующие ошибки:\n\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Ошибка валидации", error_message, parent=self.dialog)
            return
        
        # Создаем новую продукцию
        product_type = self.product_types_dict[self.new_type_var.get()]
        product_id = self.partner_request.product.create_product(
            product_type['id'],
            self.new_name_var.get().strip(),
            self.new_article_var.get().strip(),
            float(self.new_cost_var.get())
        )
        
        if product_id:
            # Добавляем в заявку
            if self.partner_request.add_product_to_request(self.request_id, product_id, int(self.new_quantity_var.get())):
                messagebox.showinfo("Успех", "Продукция успешно создана и добавлена в заявку", parent=self.dialog)
                self.dialog.destroy()
                # Обновляем список продукции
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                messagebox.showerror("Ошибка", "Продукция создана, но не удалось добавить в заявку", parent=self.dialog)
        else:
            messagebox.showerror("Ошибка", "Не удалось создать продукцию", parent=self.dialog)
