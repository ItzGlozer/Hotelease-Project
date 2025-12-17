
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setBaseSize(1280, 720)
        self.setFixedSize(1280, 720)
        # self.setMinimumSize(1280, 720)

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(24)
        self.main_layout.setContentsMargins(50, 20, 50, 50)
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def theThreeHorsemen(self, topbar, sidebar, main):
        topbar.setStyleSheet("QFrame {background: #d8d4ea; border-radius:14px;}")
        sidebar.setStyleSheet("QFrame {background: #d8d4ea; border-radius:14px;}")
        main.setStyleSheet("QFrame {background: #d8d4ea; border-radius:14px;}")

        # Add widgets
        self.main_layout.addWidget(topbar, 0, 0, 1, 2)  # row 0, span 2 columns
        self.main_layout.addWidget(sidebar, 1, 0)
        self.main_layout.addWidget(main, 1, 1)

        # Row stretch → height proportions
        self.main_layout.setRowStretch(0, 1)  # 20%
        self.main_layout.setRowStretch(1, 9)  # 80%

        # Column stretch → width proportions
        self.main_layout.setColumnStretch(0, 2)  # 20%
        self.main_layout.setColumnStretch(1, 8)  # 80%
