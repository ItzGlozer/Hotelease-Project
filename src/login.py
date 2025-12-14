from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout, QLabel
import sys

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

    def __init__(self):
        super().__init__()
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
        username = str(self.username.text())
        password = str(self.password.text())

        if username.strip() == "" or password.strip() == "":
            # ignore if a field is empty
            return

        # DEBUG
        if password.strip() == "12345":
            credentials = {
                "username": username,
                "password": password,
            }
            self.switch(credentials)


    def switch(self, credentials: dict):
        self.close()

        main_window = MainWindow(credentials)
        main_window.showMaximized()

