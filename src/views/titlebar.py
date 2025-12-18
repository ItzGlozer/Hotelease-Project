from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy

from src.resource.builder import Build


class TitleBar(QFrame):
    __STYLES = """
    QFrame {background: #d8d4ea; border-radius:14px;}
    QLabel {font-size: 36px;}
    """
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(100)

        # Create a QLabel to display the logo
        # logo
        logo_label = QLabel(self)
        pixmap = QPixmap("./asset/logo.png")  # Replace with your logo's file path
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Optional: center the logo inside the frame

        scaled_pixmap = pixmap.scaled(QSize(100, 100), Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(scaled_pixmap)

        # title
        self._title: QLabel = Build.widget(QLabel, 'title', 'Hotelease')


        # layout
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(logo_label)
        layout.addWidget(self._title)

        self.setStyleSheet(self.__STYLES)