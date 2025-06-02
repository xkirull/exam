"""Модуль для управления подключением к базе данных"""
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox


class DatabaseConnection:
    """Класс для управления подключением к базе данных"""
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='user2',
                user='root',
                password='',
                charset='utf8mb4'
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных:\n{str(e)}")
            return False
    
    def disconnect(self):
        """Закрытие соединения с базой данных"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Выполнение запроса к базе данных"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            messagebox.showerror("Ошибка запроса", f"Ошибка при выполнении запроса:\n{str(e)}")
            return None
    
    def execute_update(self, query, params=None):
        """Выполнение запроса на изменение данных"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("Ошибка обновления", f"Ошибка при обновлении данных:\n{str(e)}")
            return False
    
    def execute_insert(self, query, params=None):
        """Выполнение запроса на вставку данных с возвратом ID"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("Ошибка вставки", f"Ошибка при добавлении данных:\n{str(e)}")
            return None
