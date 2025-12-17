from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from src.model.equipment_repository import EquipmentRepository
from src.model.user_data import UserData
from src.resource.builder import Build


class DashboardAdmin(QWidget):
    __STYLES = """
    QPushButton {background: #000000;}
    QTableWidget {background: #9c9bdb;}
    QHeaderView::section {background: #8f8fd6}

    """

    def __init__(self):
        super().__init__()
        """
        Overview
        """
        # scoop
        self._staff_btn = self.__abstractOverviewCard("Staffs:")
        self._low_stock_btn = self.__abstractOverviewCard("Low Stock:")
        self._pending_request_btn = self.__abstractOverviewCard("Pending Request:")
        overview_layout = Build.flex(self._staff_btn, self._low_stock_btn, self._pending_request_btn)


        """
        Headline 
        """
        self._user_profile_display = self.__buildUserProfileDisplay()
        self._low_stock_display = self.__buildLowStockDisplay()
        self._recent_request_display = self.__buildRecentRequestDisplay()

        headline_layout = Build.flex(self._user_profile_display, self._low_stock_display, self._recent_request_display)
        headline_layout.setContentsMargins(75, 0, 75, 0)


        # layout
        self.setStyleSheet(self.__STYLES)
        main_layout = Build.flex(direction="column", parent=self)
        main_layout.addLayout(overview_layout)
        main_layout.addLayout(headline_layout)


    """
    WRAPPER HELPER
    """
    def __abstractOverviewCard(self, text) -> QPushButton:
        card = QPushButton(text)
        card.setMaximumSize(250,200)
        return card


    def __abstractHeadlineContainer(self) -> QFrame:
        container = QFrame()
        container.setStyleSheet("border: 3px solid black;")
        container.setMaximumSize(300, 350)

        return container

    def __buildUserProfileDisplay(self) -> QFrame:
        container = self.__abstractHeadlineContainer()

        full_name = f"{UserData.lastname}, {UserData.firstname}"
        name_lbl = Build.widget(QLabel, object_id="name", text=full_name)
        role_lbl = Build.widget(QLabel, object_id="role", text=UserData.role)

        Build.flex(name_lbl, role_lbl, direction="column", parent=container, alignment=Qt.AlignmentFlag.AlignHCenter)

        return container

    def __buildLowStockDisplay(self) -> QFrame:
        container = self.__abstractHeadlineContainer()
        container.setMaximumWidth(400)

        # TABLE
        self._table = QTableWidget()
        HEADERS = ["ID", "Name", "Qty."]
        self._table.setColumnCount(len(HEADERS))
        self._table.setHorizontalHeaderLabels(HEADERS)
        self._table.verticalHeader().setVisible(False)
        # col size
        self._table.setColumnWidth(0, 50)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._table.setColumnWidth(2, 50)


        layout = QVBoxLayout(container)
        layout.addWidget(self._table)


        return container

    def __buildRecentRequestDisplay(self) -> QFrame:
        container = self.__abstractHeadlineContainer()


        return container




    """
    EVENT
    """
    def default(self):
        ...

    def preload(self):
        self.loadLowStocks()


    def loadLowStocks(self):
        equipments = EquipmentRepository.fetchAllLowStocks()
        # for card overview
        self.updateLowStocks(len(equipments))

        # for headline table

        for equipment in equipments:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, key in enumerate(equipment.keys()):
                self._table.setItem(row, col, QTableWidgetItem(str(equipment[key])))


    def __updateLabelCount(self, label, count):
        text = label.text()
        index = text.find(':')
        label.setText(f"{text[:index + 1]} {count}")

    def updateStaffCount(self, count):
        self.__updateLabelCount(self._staff_btn, count)

    def updateLowStocks(self, count):
        self.__updateLabelCount(self._low_stock_btn, count)

    def updatePendingRequests(self, count):
        self.__updateLabelCount(self._pending_request_btn, count)

