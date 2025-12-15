
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from src.controller import Controller
from src.app import App
from src.login import Login
from src.main_window import MainWindow





def show():


    main_window = MainWindow()
    main_window.showMaximized()
    app = App()

    controller = Controller(main_window, app)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = Login(show)

    sys.exit(app.exec())  # Start the event loop
