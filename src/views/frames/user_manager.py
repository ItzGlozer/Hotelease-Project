from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QHBoxLayout, \
    QAbstractItemView, QHeaderView, QTableWidgetItem

from src.model.user_repository import UserRepository
from src.resource.builder import Build


class UserManager(QWidget):
    __STYLES = """
    QLabel {max-height: 40px;}
    QLabel#title {font-size: 36px; max-height: 40px;}
    QLineEdit, QPushButton {
    background: #8f8fd6;
    border: 2px solid black;
    border-radius: 9px;
    height: 40px;
    }
    QTableWidget {background: #9c9bdb; max-height: 400px;}
    
    QHeaderView::section {background: #8f8fd6}
    
    """
    __HEADERS = ["ID", "Name", "Position"]

    def __init__(self):
        super().__init__()

        # title
        title =Build.widget(QLabel, object_id="title", text="User Management")


        # toolbar
        # search
        self._search_user = Build.widget(QLineEdit, placeholder="Search User")
        self._search_user.setMaximumWidth(150)
        self._add_user = Build.widget(QPushButton, text="Add User")
        self._add_user.setMaximumWidth(150)

        toolbar_layout = Build.flex(self._search_user, self._add_user)
        # toolbar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # table
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(UserManager.__HEADERS)
        self._table.verticalHeader().setVisible(False)
        # col size
        self._table.setColumnWidth(0, 25)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        for col in range(1, self._table.columnCount()):
            self._table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        self._table.setMaximumWidth(1000)
        self._table.setMinimumHeight(350)
        table_layout = Build.flex(self._table)


        # layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 50, 20, 250)
        main_layout.setSpacing(25)
        main_layout.addWidget(title)
        main_layout.addLayout(toolbar_layout)
        main_layout.addLayout(table_layout)


        self.setStyleSheet(self.__STYLES)


    def default(self):
        users = UserRepository.fetchAll()
        for user in users:
            row = self._table.rowCount()
            self._table.insertRow(row)

            self._table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
            full_name = f"{user['firstname']} {user['lastname']}"
            self._table.setItem(row, 1, QTableWidgetItem(full_name))
            self._table.setItem(row, 2, QTableWidgetItem(str(user["role"]).capitalize()))