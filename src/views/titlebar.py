from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton


class TitleBar(QFrame):
    def __init__(self):
        super().__init__()

        # widget
        self._title = QLabel('HotelEase')

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._title)
