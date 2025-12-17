
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from src.model.equipment_repository import EquipmentRepository
from src.resource.builder import Build


class Inventory(QWidget):
    __STYLES = """
    QLineEdit, QComboBox {height: 32px; padding-left: 10px;}
    QPushButton {height: 24px}
    QWidget {
            background: #8f8fd6;
    }
    QLabel {background: transparent;}

    QTableWidget {
        background-color: #9c9bdb;
    }
    """
    __headers = ["ID", "Name", "Qty.", "Status"]

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        # self.setContentsMargins(20, 20, 20 ,20)
        self.setMaximumSize(1200, 700)
        self.setStyleSheet(Inventory.__STYLES)

        # title
        title = QLabel("Admin Inventory")
        title.setStyleSheet("font-size: 34px; max-height: 40px;")

        """
        SEARCH BAR
        """
        # search
        self._search_field: QLineEdit = Build.widget(QLineEdit, placeholder="Search")
        self._search_field.setMaximumWidth(150)
        self._search_btn = QPushButton("O")
        self._search_btn.setMaximumWidth(36)
        search_layout = Build.flex(self._search_field, self._search_btn)
        search_layout.setSpacing(0)

        # status dropdown
        self._status = Build.widget(QComboBox, items=["All Status", "In Stock", "Low Stock", "Out of Stock"])
        self._status.setMaximumWidth(100)
        searchbar_layout = Build.flex(search_layout, "stretch", self._status)

        """
        TOOLBAR
        """
        self._add_btn = Build.widget(QPushButton, "toolbar", "+")
        self._update_btn = Build.widget(QPushButton, "toolbar", "O")
        self._delete_btn = Build.widget(QPushButton, "toolbar", "-")
        toolbar_layout = Build.flex(self._add_btn, "stretch", self._update_btn, self._delete_btn)


        """
        TABLE
        """
        self._table = QTableWidget()
        self._table.setColumnCount(len(Inventory.__headers))
        self._table.setHorizontalHeaderLabels(self.__headers)
        self._table.verticalHeader().setVisible(False)

        # col size
        self._table.setColumnWidth(0, 75)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._table.setColumnWidth(2, 75)
        self._table.setColumnWidth(3, 200)


        # layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.addWidget(title)
        main_layout.addLayout(searchbar_layout)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self._table)


    def connectSignals(self):
        self._add_btn.clicked.connect(self._openForm)


    def _openForm(self):
        self._parent.showOverlay("add equipment")


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
    def default(self):
        ...

    def preload(self):
        self.loadInventory()


    def loadInventory(self):
        equipments = EquipmentRepository.fetchAll()
        self._table.setRowCount(0)

        for equipment in equipments:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, key in enumerate(equipment.keys()):
                item_widget = QTableWidgetItem(str(equipment[key]))
                self._table.setItem(row, col, item_widget)

            # for action DEBUG
            item_widget = QTableWidgetItem("No Actions")
            self._table.setItem(row, 3, item_widget)





