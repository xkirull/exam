"""Окно редактирования заявки"""
import tkinter as tk
from tkinter import ttk, messagebox
from utils.styles import AppStyles
from utils.validators import Validators


class EditWindow:
    """Окно редактирования/добавления заявки"""
    
    def __init__(self, parent, partner_request, request_data=None, refresh_callback=None):
        self.parent = parent
        self.partner_request = partner_request
        self.request_data = request_data
        self.refresh_callback = refresh_callback  # Добавляем callback для обновления
        self.is_edit = request_data is not None
        
        # Создание окна
        self.window = tk.Toplevel(parent)
        self.window.title(self._get_window_title())
        self.window.geometry("600x550")
        self.window.configure(bg=AppStyles.MAIN_BG)
        
        # Делаем окно модальным
        self.window.transient(parent)
        self.window.grab_set()
        
        # Центрируем окно
        self._center_window()
        
        # Создаем интерфейс
        self._create_widgets()
    
    def _get_window_title(self):
        """Получение заголовка окна"""
        if self.is_edit:
            return f"Редактирование заявки №{self.request_data['request_id']} - Новые технологии"
        return "Добавление новой заявки - Новые технологии"
    
    def _center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 600) // 2
        y = (self.window.winfo_screenheight() - 550) // 2
        self.window.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Создание виджетов окна"""
        # Заголовок
        header_text = "Редактирование заявки партнера" if self.is_edit else "Добавление новой заявки"
        header_label = tk.Label(
            self.window,
            text=header_text,
            font=(AppStyles.MAIN_FONT, 18, 'bold'),
            bg=AppStyles.MAIN_BG,
            fg=AppStyles.ACCENT_COLOR
        )
        header_label.pack(pady=(20, 10))
        
        # Форма
        self.form_frame = tk.Frame(self.window, bg=AppStyles.MAIN_BG)
        self.form_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
        
        # Получаем типы партнеров
        partner_types = self.partner_request.partner.get_partner_types()
        self.partner_types_dict = {pt['type_name']: pt['id'] for pt in partner_types}
        
        # Создаем поля формы
        self.fields = {}
        self._create_form_fields()
        
        # Кнопки
        self._create_buttons()
    
    def _create_form_fields(self):
        """Создание полей формы"""
        # Данные для полей
        fields_data = [
            ('partner_type', 'Тип партнера:', 'combobox', list(self.partner_types_dict.keys())),
            ('company_name', 'Наименование:', 'entry', None),
            ('director_name', 'ФИО директора:', 'entry', None),
            ('legal_address', 'Адрес:', 'entry', None),
            ('inn', 'ИНН:', 'entry', None),
            ('rating', 'Рейтинг:', 'entry', None),
            ('phone', 'Телефон:', 'entry', None),
            ('email', 'Email:', 'entry', None),
        ]
        
        for row, (field_name, label_text, field_type, values) in enumerate(fields_data):
            # Метка
            label = tk.Label(
                self.form_frame, 
                text=label_text, 
                font=(AppStyles.MAIN_FONT, 12), 
                bg=AppStyles.MAIN_BG
            )
            label.grid(row=row, column=0, sticky='w', pady=5)
            
            # Поле ввода
            if field_type == 'combobox':
                var = tk.StringVar()
                widget = ttk.Combobox(
                    self.form_frame, 
                    textvariable=var, 
                    style='Custom.TCombobox', 
                    state='readonly'
                )
                widget['values'] = values
                if self.is_edit:
                    var.set(self.request_data.get('partner_type', ''))
                else:
                    widget.current(0)
            else:
                var = tk.StringVar()
                widget = ttk.Entry(
                    self.form_frame, 
                    textvariable=var, 
                    style='Custom.TEntry'
                )
                if self.is_edit:
                    default_value = self.request_data.get(field_name, '')
                    if field_name == 'rating':
                        default_value = str(default_value)
                    var.set(default_value)
                elif field_name == 'rating':
                    var.set('0')
            
            widget.grid(row=row, column=1, sticky='ew', pady=5, padx=(10, 0))
            self.fields[field_name] = var
        
        # Настройка колонок
        self.form_frame.columnconfigure(1, weight=1)
    
    def _create_buttons(self):
        """Создание кнопок"""
        button_frame = tk.Frame(self.window, bg=AppStyles.MAIN_BG)
        button_frame.pack(pady=(0, 20))
        
        save_text = "Сохранить" if self.is_edit else "Создать"
        save_button = ttk.Button(
            button_frame,
            text=save_text,
            style='Action.TButton',
            command=self._save
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame,
            text="Отмена",
            style='Action.TButton',
            command=self.window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def _validate_fields(self):
        """Валидация полей формы"""
        errors = []
        
        # Проверка заполненности обязательных полей
        if not self.fields['company_name'].get().strip():
            errors.append("Наименование компании не может быть пустым")
        
        if not self.fields['director_name'].get().strip():
            errors.append("ФИО директора не может быть пустым")
        
        if not self.fields['legal_address'].get().strip():
            errors.append("Адрес не может быть пустым")
        
        # Валидация рейтинга
        if not Validators.validate_rating(self.fields['rating'].get()):
            errors.append("Рейтинг должен быть целым неотрицательным числом")
        
        # Валидация email
        if not Validators.validate_email(self.fields['email'].get()):
            errors.append("Некорректный формат email адреса")
        
        # Валидация телефона
        if not Validators.validate_phone(self.fields['phone'].get()):
            errors.append("Телефон должен содержать не менее 10 цифр")
        
        # Валидация ИНН
        if not Validators.validate_inn(self.fields['inn'].get()):
            errors.append("ИНН должен состоять из 10 цифр")
        
        return errors
    
    def _save(self):
        """Сохранение данных"""
        # Валидация
        errors = self._validate_fields()
        if errors:
            error_message = "Обнаружены следующие ошибки:\n\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Ошибка валидации", error_message, parent=self.window)
            return
        
        # Подтверждение для редактирования
        if self.is_edit:
            if not messagebox.askyesno("Подтверждение", 
                                      "Вы уверены, что хотите сохранить изменения?", 
                                      parent=self.window):
                return
        
        # Подготовка данных
        partner_type_id = self.partner_types_dict[self.fields['partner_type'].get()]
        
        if self.is_edit:
            # Обновление существующего партнера
            success = self.partner_request.partner.update_partner(
                self.request_data['partner_id'],
                partner_type_id,
                self.fields['company_name'].get().strip(),
                self.fields['director_name'].get().strip(),
                self.fields['email'].get().strip(),
                self.fields['phone'].get().strip(),
                self.fields['legal_address'].get().strip(),
                self.fields['inn'].get().strip(),
                int(self.fields['rating'].get())
            )
            
            if success:
                messagebox.showinfo("Успех", "Данные успешно сохранены", parent=self.window)
                self.window.destroy()
                # Вызываем callback для обновления списка
                if self.refresh_callback:
                    self.refresh_callback()
        else:
            # Создание нового партнера и заявки
            partner_id = self.partner_request.partner.create_partner(
                partner_type_id,
                self.fields['company_name'].get().strip(),
                self.fields['director_name'].get().strip(),
                self.fields['email'].get().strip(),
                self.fields['phone'].get().strip(),
                self.fields['legal_address'].get().strip(),
                self.fields['inn'].get().strip(),
                int(self.fields['rating'].get())
            )
            
            if partner_id:
                request_id = self.partner_request.create_request(partner_id)
                if request_id:
                    messagebox.showinfo("Успех", f"Заявка №{request_id} успешно создана", parent=self.window)
                    self.window.destroy()
                    # Вызываем callback для обновления списка
                    if self.refresh_callback:
                        self.refresh_callback()
                else:
                    messagebox.showerror("Ошибка", "Не удалось создать заявку", parent=self.window)
            else:
                messagebox.showerror("Ошибка", "Не удалось создать партнера", parent=self.window)
