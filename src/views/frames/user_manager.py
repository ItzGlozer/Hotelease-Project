from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QHBoxLayout, \
    QAbstractItemView, QHeaderView, QTableWidgetItem, QComboBox, QMessageBox

from src.model.user_repository import UserRepository
from src.resource.builder import Build


class UserManager(QWidget):
    __STYLES = """
    QLabel#title {font-size: 36px; max-height: 40px;}
    QLineEdit, QComboBox, QPushButton {
    background: #8f8fd6;
    border: 2px solid black;
    border-radius: 9px;
    max-width: 150px;
    font-size: 18px;
    }
    QLineEdit, QComboBox {padding: 2 0 2 10;}
    QPushButton {padding: 5 0 5 0;}
    QPushButton:hover {background: #c6bce6;}
    QPushButton:pressed {background: #A0F}
    QTableWidget {background: #9c9bdb;}
    QTableWidget::item:selected {background: #A0F; color: white;}
    QHeaderView::section {background: #8f8fd6}

    """
    __HEADERS = ["ID", "Name", "Position"]

    _cell_selected = None

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        title = Build.widget(QLabel, 'title', "User Manager")

        """
        LEFT PANEL
        """
        self._add_btn = QPushButton("Add User")
        self._update_btn = QPushButton("Update User")
        self._delete_btn = QPushButton("Delete User")

        left_layout = Build.flex(self._add_btn, self._update_btn, self._delete_btn, direction='column')


        """
        RIGHT PANEL
        """
        # SEARCH BAR
        # search by name
        self._search_field: QLineEdit = Build.widget(QLineEdit, placeholder="Search by name")

        # role dropdown
        self._role_dropdown: QComboBox = Build.widget(QComboBox, items=['All Positions', 'Admin', 'Staff'])

        search_layout = Build.flex(self._search_field, self._role_dropdown)

        # TABLE
        self._table = QTableWidget()
        self._table.setColumnCount(len(UserManager.__HEADERS))
        self._table.setHorizontalHeaderLabels(UserManager.__HEADERS)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setMaximumWidth(400)

        # col size
        self._table.setColumnWidth(0, 50)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # self._table.setColumnWidth(2, 75)
        # self._table.setColumnWidth(3, 200)

        right_layout = Build.flex(search_layout, self._table, direction='column')


        content_layout = Build.flex(left_layout, right_layout)

        main_layout = QVBoxLayout(self)

        main_layout.addWidget(title)
        main_layout.addLayout(content_layout)

        self.setStyleSheet(self.__STYLES)

    """
    UTILITY
    """
    def connectSignals(self, controller):
        self._add_btn.clicked.connect(lambda _: self._openForm('add user'))
        self._update_btn.clicked.connect(self._update)
        self._delete_btn.clicked.connect(lambda _: self._delete(controller))
        self._table.cellClicked.connect(self._cellClicked)
        self._search_field.textChanged.connect(self._searchOnTextChanged)
        self._role_dropdown.currentTextChanged.connect(self._searchOnTextSelected)

    def default(self):
        ...

    def preload(self):
        self.loadUsers()

    def _openForm(self, form_name):
        self._parent.showOverlay(form_name)


    """
    FRONTEND
    """
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

            item = self._table.item(row, 2)

            if item and to_search == item.text().lower():
                match_found = True
            elif to_search == 'all positions':
                match_found = True

            self._table.setRowHidden(row, not match_found)


    def _cellClicked(self, row, col):
        self._cell_selected = {
            'id': self._table.item(row, 0).text(),
            'name': self._table.item(row, 1).text(),
        }

    def _openForm(self, frame_name, pre_data=None):
        self._parent.showOverlay(frame_name, pre_data)

    """
    BACKEND
    """
    def loadUsers(self):
        # ensures table is empty before inserting data
        self._table.setRowCount(0)

        users = UserRepository.fetchAll()
        for user in users:
            row = self._table.rowCount()
            self._table.insertRow(row)

            self._table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
            full_name = f"{user['firstname']} {user['lastname']}"
            self._table.setItem(row, 1, QTableWidgetItem(full_name))
            self._table.setItem(row, 2, QTableWidgetItem(str(user["role"]).capitalize()))

    def _update(self):
        pre_data = self._cell_selected

        if pre_data is None:
            # prompt user to select a user
            QMessageBox.warning(None, 'Warning', 'Please select a user.')
            return

        self._openForm('update user', pre_data)

    def _delete(self, controller):
        userdata = self._cell_selected

        if userdata is None:
            # prompt user to select a user
            QMessageBox.warning(None, 'Warning', 'Please select a user.')
            return

        msg = QMessageBox()
        msg.setWindowTitle('Deletion')
        msg.setText(f"Confirm to delete\nuser: {userdata['name']}")

        yes_btn = msg.addButton("Confirm", QMessageBox.ButtonRole.YesRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.NoRole)

        msg.exec()

        if msg.clickedButton() == yes_btn:
            QMessageBox.information(None, 'Deletion', "Deleting user\nPress OK to continue.")
            controller.deleteUserdata(userdata) # send to database
            self.loadUsers() # reload able
            QMessageBox.information(None, 'Deletion', "User Deleted\nTable has been refresh.")

        # reset selected cell after prompt
        self._cell_selected = None
