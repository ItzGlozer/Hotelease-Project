
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from src.resource.builder import Build


class Inventory(QWidget):
    __headers = ["ID", "Name", "Qty.", "Status", "Actions"]

    def __init__(self):
        super().__init__()
        self.setContentsMargins(20, 20, 20 ,20)
        self.setStyleSheet("""
        QWidget {
            background: #8f8fd6;
        }
        QLabel {background: transparent;}

        QTableWidget {
            background-color: #9c9bdb;
        }
        """)

        # title
        title = QLabel("Admin Inventory")
        title.setStyleSheet("font-size: 34px; max-height: 40px;")


        # toolbar
        self._search_id = QLineEdit("Search ID")
        self._search_name = QLineEdit("Search Name")
        self._status = Build.widget(QComboBox, items=["All Status", "In Stock", "Low Stock", "Out of Stock"])
        self._add = Build.widget(QPushButton, text="Add Equipment")

        tools = [self._search_id, self._search_name, self._status, self._add]
        toolbar_layout = Build.flex(*tools)
        self.__configTools(tools)


        # table
        self._table = QTableWidget()
        self._table.setColumnCount(len(Inventory.__headers))
        self._table.setHorizontalHeaderLabels(self.__headers)
        self._table.verticalHeader().setVisible(False)

        # col size
        self._table.setColumnWidth(0, 25)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        for col in range(1, self._table.columnCount()):
            self._table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)



        # layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self._table)


    """
    HELPER
    """
    def __configTools(self, widgets: list):
        for widget in widgets:
            widget.setMinimumHeight(50)
            widget.setMaximumWidth(230)
            widget.setStyleSheet("""
                padding-left: 10px;
                border: 2px solid black;
                background: #8f8fd6;
                border-radius: 5px;
            """)


    """
    EVENT
    """
    def appendData(self, data: list | tuple):
        row = self._table.rowCount()
        self._table.insertRow(row)

        for col, item in enumerate(data):
            item_widget = QTableWidgetItem(str(item))
            item_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._table.setItem(row, col, item_widget)


