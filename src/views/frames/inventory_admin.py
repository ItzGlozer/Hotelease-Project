
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from src.model.equipment_repository import EquipmentRepository
from src.resource.builder import Build


class InventoryAdmin(QWidget):
    __STYLES = """
    QLineEdit, QComboBox {height: 32px; padding-left: 10px;}
    QPushButton {height: 24px}
    QPushButton:hover {background: #c6bce6;}
    QPushButton:pressed {background: #A0F}
    QWidget {background: #8f8fd6;}
    QLabel {background: transparent;}
    QTableWidget {background-color: #9c9bdb;}
    QTableWidget::item:selected {background: #A0F; color: white;}
    """
    __headers = ["ID", "Name", "Qty.", "Status"]
    _cell_selected = None

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        # self.setContentsMargins(20, 20, 20 ,20)
        self.setMaximumSize(1200, 700)
        self.setStyleSheet(InventoryAdmin.__STYLES)

        # title
        title = QLabel("Admin Inventory")
        title.setStyleSheet("font-size: 34px; max-height: 40px;")

        """
        SEARCH BAR
        """
        # search
        self._search_field: QLineEdit = Build.widget(QLineEdit, placeholder="Search")
        self._search_field.setMaximumWidth(150)

        # status dropdown
        self._status: QComboBox = Build.widget(QComboBox, items=["All Status", "In Stock", "Low Stock", "Out of Stock"])
        self._status.setMaximumWidth(100)
        searchbar_layout = Build.flex(self._search_field, "stretch", self._status)

        """
        TOOLBAR
        """
        self._add_btn = Build.widget(QPushButton, "toolbar", "+")
        self._delete_btn = Build.widget(QPushButton, "toolbar", "-")
        toolbar_layout = Build.flex(self._add_btn, "stretch", self._delete_btn)


        """
        TABLE
        """
        self._table = QTableWidget()
        self._table.setColumnCount(len(InventoryAdmin.__headers))
        self._table.setHorizontalHeaderLabels(self.__headers)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

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
    UTILITY
    """
    def connectSignals(self, controller):
        self._search_field.textChanged.connect(self._searchOnTextChanged)
        self._status.currentTextChanged.connect(self._searchOnTextSelected)
        self._add_btn.clicked.connect(self._openForm)
        self._delete_btn.clicked.connect(lambda _: self._promptDeletion(controller))
        self._table.cellClicked.connect(self._cellClicked)

    def default(self):
        ...

    def preload(self):
        self.loadInventory()


    """
    FRONTEND
    """


    def _openForm(self):
        self._parent.showOverlay("add equipment")

    def _searchOnTextChanged(self, text):
        to_search = text.lower()
        for row in range(self._table.rowCount()):
            match_found = False

            item = self._table.item(row, 1)

            if item and to_search in item.text().lower():
                match_found = True

            self._table.setRowHidden(row, not match_found)

    def _searchOnTextSelected(self, text):
        to_search = text.lower()
        for row in range(self._table.rowCount()):
            match_found = False

            item = self._table.item(row, 3)

            if item and to_search == item.text().lower():
                match_found = True
            elif to_search == 'all status':
                match_found = True

            self._table.setRowHidden(row, not match_found)

    def _cellClicked(self, row, column):
        self._cell_selected = {
            'id': self._table.item(row, 0).text(),
            'name': self._table.item(row, 1).text(),
        }


    """
    BACKEND
    """
    def _promptDeletion(self, controller):

        if self._cell_selected is None:
            # prompt user if there is no selected cell
            QMessageBox.warning(self, "Warning", "Please select an equipment")
            return

        msg = QMessageBox()
        msg.setWindowTitle("Deletion")
        msg.setText(f"Confirm to delete\nequipment: {self._cell_selected['name']}")

        yes_btn = msg.addButton("Confirm", QMessageBox.ButtonRole.YesRole)
        no_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.NoRole)

        msg.exec()

        if msg.clickedButton() == yes_btn:
            QMessageBox.information(self, "Info", "Deletion will begin shortly\nPress OK to continue")
            status = controller.deleteEquipment(self._cell_selected) # send to database
            if status:
                self.loadInventory() # reload table
                QMessageBox.information(self, "Info", "Successfully Deleted\nTable is now refreshed.")
            else:
                QMessageBox.warning(self, "Warning", "Deletion failed\nEquipment is used in request logs.")

        # reset selected cell after prompt
        self._cell_selected = None


    @staticmethod
    def __validateStock(quantity) -> str:
        try:
            if int(quantity) <= 0:
                return 'Out of Stock'
            elif int(quantity) <= 20:
                return 'Low Stock'
            else:
                return 'In Stock'
        except TypeError:
            # if quantity is None/Null then it must be newly created
            return 'Out of Stock'

    def loadInventory(self):
        equipments = EquipmentRepository.fetchAll()

        # ensures table is empty before inserting data
        self._table.setRowCount(0)

        for equipment in equipments:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, key in enumerate(equipment.keys()):
                self._table.setItem(row, col, QTableWidgetItem(str(equipment[key])))

            # status column
            status = InventoryAdmin.__validateStock(equipment['quantity'])
            self._table.setItem(row, 3, QTableWidgetItem(status))







