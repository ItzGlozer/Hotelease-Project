from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import *

from src.model.equipment_repository import EquipmentRepository
from src.resource.builder import Build


class InventoryStaff(QWidget):
    __STYLES = """
    QLabel {font-size: 32px;}
    QLineEdit, QPushButton {
    background: #7a7ad5;
    border: 2px solid #1E1E1E;
    border-radius: 5px;
    }
    QLineEdit {font-size: 16px;}
    QPushButton {font-size: 18px; padding: 5 20 5 20}
    QPushButton:hover {background: #c6bce6;}
    QPushButton:pressed {background: #A0F}
    QHeaderView::section {background: #8f8fd6}
    QTableWidget {background-color: #9c9bdb;}
    QTableWidget::item:selected {background: #A0F; color: white;}
    """
    __HEADERS = ["ID", "Name", "Qty."]

    _cell_selected: dict = None

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setStyleSheet(self.__STYLES)

        # TITLE HEADER
        title = QLabel("Inventory Staff")

        """
        TOOLBAR
        """
        # search
        self._search_field = Build.widget(QLineEdit, placeholder="Search by name")
        self._search_field.textChanged.connect(self._searchOnTextChanged)
        self._search_field.setMaximumWidth(162)
        self._search_field.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # request btn
        self._request_btn = Build.widget(QPushButton, text="Open a Request")
        self._request_btn.clicked.connect(self._openRequest)
        toolbar_layout = Build.flex("stretch", self._search_field, self._request_btn, "stretch", direction="column")


        # table
        self._table = QTableWidget()
        self._table.setColumnCount(len(self.__HEADERS))
        self._table.setHorizontalHeaderLabels(self.__HEADERS)
        self._table.verticalHeader().setVisible(False)
        self._table.cellClicked.connect(self._cellClicked)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setMaximumWidth(400)

        # col size
        self._table.setColumnWidth(0, 75)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._table.setColumnWidth(2, 75)


        # layout
        central_layout = QHBoxLayout()
        central_layout.addLayout(toolbar_layout)
        central_layout.addWidget(self._table)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addLayout(central_layout)

    """
    UTILITY
    """
    def default(self):
        ...

    def preload(self):
        self.loadInventory()

    """
    FRONTEND
    """
    def connectSignals(self, controller):
        ...

    def _cellClicked(self, row, col):
        self._cell_selected = {
            "id": self._table.item(row, 0).text(),
            "name": self._table.item(row, 1).text(),
            "quantity": self._table.item(row, 2).text(),
        }

    def _searchOnTextChanged(self):
        to_search = self._search_field.text().lower()

        for row in range(self._table.rowCount()):
            match_found = False

            for col in range(self._table.columnCount()):
                item = self._table.item(row, col)
                if item and to_search in item.text().lower():
                    match_found = True
                    break

            self._table.setRowHidden(row, not match_found)

    def _openRequest(self):
        if self._cell_selected is None:
            QMessageBox.warning(None, "Warning", "Please select a cell")

        else:
            # open overlay with form and pass in cell data selected
            self._parent.showOverlay('add request', self._cell_selected)
            # clear cell selected after passing
            self._cell_selected = None


    """
    BACKEND
    """
    def loadInventory(self):
        equipments = EquipmentRepository.fetchAll()

        for equipment in equipments:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, key in enumerate(equipment.keys()):
                self._table.setItem(row, col, QTableWidgetItem(str(equipment[key])))





