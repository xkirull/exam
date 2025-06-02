"""Точка входа в приложение"""
from views.main_window import MainWindow


def main():
    """Запуск приложения"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
