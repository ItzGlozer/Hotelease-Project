
import sys
from PyQt6.QtWidgets import QApplication


from src.login import Login

if __name__ == '__main__':
    q_app = QApplication(sys.argv)

    login = Login()

    sys.exit(q_app.exec())