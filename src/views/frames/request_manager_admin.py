from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QComboBox, QTableWidget, QPushButton,
                             QHeaderView)

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
    __HEADERS = ["ID", "Item Requested", "Qty.", "Requested By", "Status", "Date", "Action"]

    def __init__(self):
        super().__init__()

        # title
        title = QLabel("Request Management")


        # toolbar
        self._status_selection = Build.widget(QComboBox, items=["All Request", "Pending", "Approved", "Denied"])
        self._approve_btn = QPushButton("Approve")
        self._deny_btn = QPushButton("Deny")
        tools = [self._status_selection, self._approve_btn, self._deny_btn]
        self._configTools(tools)
        toolbar_layout = Build.flex(*tools)


        # table
        self._table = QTableWidget()
        self._table.setMaximumWidth(1300)
        self._table.setColumnCount(len(self.__HEADERS))
        self._table.setHorizontalHeaderLabels(self.__HEADERS)
        self._table.verticalHeader().setVisible(False)

        # col size
        self._table.setColumnWidth(0, 25)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        for col in range(1, self._table.columnCount()):
            self._table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        # layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 50, 0, 0)
        main_layout.setSpacing(50)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(title)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self._table)

        self.setStyleSheet(self.__STYLES)


    """
    HELPER FUNCTIONS
    """
    def _configTools(self, tools):

        for tool in tools:
            tool.setMaximumWidth(150)
            tool.setStyleSheet("""
            background-color: #8f8fd6;
            border: 2px solid black;
            border-radius: 9px;
            height: 42px;
            padding: 0 10px
            """)



    """
    EVENT
    """


    """
    FETCH
    """
    def loadRequest(self):
        ...

    """
    FRONTEND
    """
    def connectSignals(self):
        ...

    """
    BACKEND
    """

