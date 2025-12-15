from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout, QLabel, QMessageBox
import sys

from src.model.user_data import UserData
from src.model.user_repository import UserRepository
from src.resource.builder import Build
from src.main_window import MainWindow

class Login(QWidget):
    __STYLES = """
    QWidget {background: #d8d4ea; font-family: Times New Roman;}
    QLabel {font-size: 24px;}
    QLineEdit {
        padding-left: 9px;
        color: gray;
        background: white;
        border-radius: 24px;
    }
    QPushButton {
        background: #8f8fd6;
        border: 2px solid black;
        border-radius: 9px;
        font-size: 16px;
        height: 36px;

    }
    """

    def __init__(self, callback):
        super().__init__()
        self._callback = callback

        self.setFixedSize(350,500)
        self.setWindowTitle("Login")

        # Title
        title = QLabel("Login")

        self.username: QLineEdit = Build.widget(QLineEdit, placeholder="Username", width=250, height=48)
        self.password = Build.widget(QLineEdit, placeholder="Password", width=250, height=48)

        self.login_btn = Build.widget(QPushButton, text="Login", width=200)
        self.login_btn.clicked.connect(self.validateCredentials)


        # layout
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter)


        self.setStyleSheet(self.__STYLES)
        self.show()


    def validateCredentials(self):
        credentials = {
            "username": str(self.username.text()),
            "password": str(self.password.text()),
        }

        if credentials["username"].strip() == "" or credentials["password"].strip() == "":
            # prompt if a field is empty
            QMessageBox.information(self, "Notice", "Fields must not be empty!")
            return

        # Validate data provided
        result = UserRepository.validateCredentials(credentials)
        if result:
            # proceed to app if success
            QMessageBox.information(None, "Notice", "Successfully Logged In!\nPlease wait shortly...")
            UserData(result)
            self.switch()
        else:
            # prompt if credential is invalid
            QMessageBox.information(self, "Notice", "Invalid credentials!")


    def switch(self):
        self.close()
        self._callback()

