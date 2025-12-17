from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *

from src.model.request_repository import RequestRepository
from src.model.user_data import UserData
from src.resource.builder import Build


class RequestManagerStaff(QWidget):
    __STYLES = """
    QWidget {
            background: #8f8fd6;
    }
    QLabel {background: transparent; font-size: 30px;}
    QPushButton, QComboBox {border: 1px solid #1E1E1E; border-radius: 5px;}
    QComboBox {
    font-size: 16px;
    padding: 10 0 10 5;
    width: 100px;
    }
    QPushButton {
    font-size: 24px;
    padding: 5 5 5 5;
    }
    QTableWidget {
        background-color: #9c9bdb;
    }
    """
    __HEADERS = ["ID", "Equipment", "Qty.", "Type", "Status", "Approved by", "Date", "Date Approved"]

    _is_prompted = False
    _cell_selected = None

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setStyleSheet(RequestManagerStaff.__STYLES)

        """
        TITLE
        """
        title = QLabel("My Request Manager")

        """
        TOOLBAR
        """
        self._status_dropdown: QComboBox = Build.widget(QComboBox, items=["All Status", "Pending", "Approved", "Rejected"])
        self._cancel_btn = QPushButton("Cancel Request")
        self._cancel_btn.setDisabled(True)
        tools = [self._status_dropdown, "stretch", self._cancel_btn]
        toolbar_layout = Build.flex(*tools)

        """
        TABLE
        """
        self._table = QTableWidget()
        self._table.setColumnCount(len(self.__HEADERS))
        self._table.setHorizontalHeaderLabels(self.__HEADERS)
        self._table.verticalHeader().setVisible(False)
        # size
        self._table.setMaximumHeight(400)

        # col size
        self._table.setColumnWidth(0, 75)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._table.setColumnWidth(2, 75)
        self._table.setColumnWidth(3, 75)
        self._table.setColumnWidth(4, 100)
        self._table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)


        # layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self._table)


    """
    """
    def connectSignals(self, controller):
        self._cancel_btn.clicked.connect(lambda _: self._promptCancel(controller))
        self._table.cellClicked.connect(self._cellClicked)
        self._status_dropdown.currentTextChanged.connect(self._searchOnSelectedItem)

    def _cellClicked(self, row, col):
        self._cell_selected = {
            "id": self._table.item(row, 0).text(),
            "status": self._table.item(row, 4).text(),
        }

        # enable button and shortly 10s disabled
        self._cancel_btn.setDisabled(False)
        QTimer.singleShot(7000, self._disableButton)

    """
    FRONT END
    """

    def _searchOnSelectedItem(self, to_search: str):
        for row in range(self._table.rowCount()):
            match_found = False

            item = self._table.item(row, 4)

            if item and to_search.lower() == item.text().lower():
                match_found = True
            elif to_search.lower() == 'all status':
                match_found = True

            self._table.setRowHidden(row, not match_found)

    def default(self):
        self.loadRequest()

    def _disableButton(self):
        """
        Disable the button and reset the cell selected.
        """
        self._cancel_btn.setDisabled(True)
        self._cell_selected = None



    """
    BACKEND
    """
    def _promptCancel(self, controller):
        # validate request, if request approved then prompt that cancel is unavailable
        if self._cell_selected["status"].lower() in ['approved', 'rejected']:
            QMessageBox.warning(self, "Cancel", "This request has been already managed.")
            return

        # open prompt for confirmation
        msg = QMessageBox()
        msg.setWindowTitle("Cancel Request")
        msg.setText("Confirm to cancel request.")

        yes_btn = msg.addButton("Confirm", QMessageBox.ButtonRole.YesRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.NoRole)

        msg.exec()

        if msg.clickedButton() == yes_btn:
            if self._cell_selected is None:
                # fail-safe, when selected cell has been reset, open this prompt
                QMessageBox.warning(self, "Notice", "Select a request again.")
                return
            # cancel the request through database and refresh the table
            controller.cancelRequest(self._cell_selected)
            self.loadRequest()

        self._disableButton()


    def loadRequest(self):
        requests = RequestRepository.fetchUserRequests(UserData().user_id)

        # ensures table is empty before inserting data
        self._table.setRowCount(0)

        for request in requests:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, key in enumerate(request.keys()):
                self._table.setItem(row, col, QTableWidgetItem(str(request[key])))

