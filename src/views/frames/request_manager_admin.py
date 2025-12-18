from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QComboBox, QTableWidget, QPushButton,
                             QHeaderView, QTableWidgetItem, QMessageBox)

from src.model.request_repository import RequestRepository
from src.model.user_data import UserData
from src.resource.builder import Build


class RequestManagerAdmin(QWidget):
    __STYLES = """
    QLabel {font-size: 36px; max-height: 40px;}
    
    QTableWidget {
        background-color: #9c9bdb;
        max-height: 400px;
    }
    
    QHeaderView::section {
        background: #8f8fd6
    }
    
    """
    __HEADERS = ["ID", "Equipment", "Qty.", "Type", "Status", "Requested by", "Validated by", "Requested at", "Validated at"]

    _cell_selected = None

    def __init__(self):
        super().__init__()

        # title
        title = QLabel("Request Management")


        # toolbar
        self._status_selection = Build.widget(QComboBox, items=["All Status", "Pending", "Approved", "Rejected"])
        self._approve_btn = QPushButton("Approve")
        self._reject_btn = QPushButton("Reject")
        tools = [self._status_selection, self._approve_btn, self._reject_btn]
        self._buildTools(tools)
        tools.insert(1, "stretch")
        toolbar_layout = Build.flex(*tools)


        # table
        self._table = QTableWidget()
        # self._table.setMaximumWidth(1300)
        self._table.setColumnCount(len(self.__HEADERS))
        self._table.setHorizontalHeaderLabels(self.__HEADERS)
        self._table.verticalHeader().setVisible(False)

        # col size
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        self._table.setColumnWidth(7, 100)
        self._table.setColumnWidth(8, 100)


        # layout
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 50, 0, 0)
        # main_layout.setSpacing(50)
        # main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(title)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self._table)

        self.setStyleSheet(self.__STYLES)


    """
    HELPER FUNCTIONS
    """
    def _buildTools(self, tools):
        for tool in tools:
            tool.setMaximumWidth(150)
            tool.setStyleSheet("""
            background-color: #8f8fd6;
            border: 2px solid black;
            border-radius: 9px;
            font-size: 18px;
            padding: 5 10 5 10; 
            """)




    """
    UTILITY
    """
    def connectSignals(self, controller):
        self._status_selection.currentTextChanged.connect(self._searchOnSelectChanged)
        self._approve_btn.clicked.connect(lambda _: self._submitValidation(controller, 'approved'))
        self._reject_btn.clicked.connect(lambda _: self._submitValidation(controller, 'rejected'))
        self._table.cellClicked.connect(self._cellClicked)

    def default(self):
        ...

    def preload(self):
        self.loadAllRequest()


    """
    FRONTEND
    """
    def _searchOnSelectChanged(self, to_search):
        print(to_search.lower())
        for row in range(self._table.rowCount()):
            match_found = False

            item = self._table.item(row, 4)

            if item and to_search.lower() == item.text().lower():
                match_found = True
            elif to_search.lower() == 'all status':
                match_found = True

            self._table.setRowHidden(row, not match_found)

    def _cellClicked(self, row, col):
        self._cell_selected = {
            'id': self._table.item(row, 0).text(),
            'status': self._table.item(row, 4).text(),
            'user_id': UserData.user_id
        }


    """
    BACKEND
    """
    # ["ID", "Equipment", "Qty.", "Type", "Status", "Requested by", "Validated by", "Requested at", "Validated at"]
    def __proxyLoad(self):
        from datetime import datetime
        data = [
            [1, 'Ball', 11, 'stock in', "Approved", 'Glych Phtsmgr', 'Serenity Skyarmy14', datetime.now(),
             datetime.now()],
            [2, 'Ball', 22, 'stock out', "Pending", 'Serenity Skyarmy14', None, datetime.now(), None],
            [3, 'Ball', 33, 'stock in', "Rejected", 'Serenity Skyarmy14', 'Glych Phtsmgr', datetime.now(),
             datetime.now()],
            [4, 'Ball', 44, 'stock out', "Pending", 'Glych Phtsmgr', None, datetime.now(), None],
            [5, 'Ball', 55, 'stock in', "Rejected", 'Xana Ax', 'Ax Hanabi', datetime.now(), datetime.now()],
            [6, 'Ball', 66, 'stock out', "Pending", 'Ax Hanabi', None, datetime.now(), None],
        ]

        # ensures table is empty before inserting
        self._table.setRowCount(0)

        for item in data:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, value in enumerate(item):
                self._table.setItem(row, col, QTableWidgetItem(str(value)))

    def loadAllRequest(self):
        requests = RequestRepository.fetchAllRequests()

        # ensures table is empty before inserting data
        self._table.setRowCount(0)

        for item in requests:
            row = self._table.rowCount()
            self._table.insertRow(row)

            for col, key in enumerate(item.keys()):
                self._table.setItem(row, col, QTableWidgetItem(str(item.get(key))))


    def _submitValidation(self, controller, status: str):

        if self._cell_selected is None:
            # prompt user to select a cell before validating
            self._warning = QMessageBox.warning(self, "Notice", "Please select a cell.")

        if self._cell_selected['status'].lower() != 'pending':
            # prompt user if request is already validated
            QMessageBox.warning(self, 'Validation Error', 'Request has been validated already.')
            return

        # proceed to database
        QMessageBox.information(None, 'Validation', 'Successfully Validated.\nTable will be updated shortly.')
        self._cell_selected['status'] = status # change status base on admin validation
        controller.validateRequest(self._cell_selected) # send to database
        self._cell_selected = None # reset cell selected
        self.loadAllRequest() # reload table
        QMessageBox.information(None, 'Table', 'Table has been updated!')
        print("Request has been validated.")