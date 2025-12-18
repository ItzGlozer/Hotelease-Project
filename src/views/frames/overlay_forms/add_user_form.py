from PyQt6.QtWidgets import *
from src.resource.builder import Build


class AddUserForm(QWidget):
    __STYLES = """
    QLineEdit, QComboBox {
    font-size: 18px;
    border: 1px solid #d8d4ea;
    border-radius: 5px;
    padding: 2 0 2 10;
    }
    QLabel {
    font-size: 16px;
    max-height: 16px;
    }
    QPushButton {
    font-size: 16px;
    border: 1px solid #d8d4ea;
    border-radius: 5px;
    padding: 2 0;
    }
    QPushButton:pressed {background: #A0F;}
    """

    def __init__(self, overlay):
        super().__init__()
        self._overlay = overlay


        # firstname
        firstname_lbl = Build.widget(QLabel, 'field_label', 'Firstname:')
        self._firstname_field = Build.widget(QLineEdit, placeholder='ex. Juan')
        firstname_layout = Build.flex(firstname_lbl, self._firstname_field, direction='column')

        # lastname
        lastname_lbl = Build.widget(QLabel, 'field_label', 'Lastname:')
        self._lastname_field = Build.widget(QLineEdit, placeholder='ex. Dela Cruz')
        lastname_layout = Build.flex(lastname_lbl, self._lastname_field, direction='column')

        # role dropdown
        self._role_dropdown = Build.widget(QComboBox, items=['Select Role', 'Admin', 'Staff'])

        # buttons
        self._submit_btn = Build.widget(QPushButton, text='Submit')
        self._cancel_btn = Build.widget(QPushButton, text='Cancel')
        button_layout = Build.flex(self._submit_btn, self._cancel_btn)


        # layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(firstname_layout)
        main_layout.addLayout(lastname_layout)
        main_layout.addWidget(self._role_dropdown)
        main_layout.addLayout(button_layout)


        self.setStyleSheet(self.__STYLES)



    """
    UTILITY
    """
    @property
    def __get_user_input(self) -> dict:
        return {
            'firstname': self._firstname_field.text(),
            'lastname': self._lastname_field.text(),
            'role': self._role_dropdown.currentText(),
        }

    def connectSignals(self, controller):
        self._submit_btn.clicked.connect(lambda _: self._submit(controller))
        self._cancel_btn.clicked.connect(self.__closeForm)


    """
    FRONTEND
    """
    def default(self):
        self.hide()

    def showForm(self):
        self.show()

    def __closeForm(self):
        """
        Hide the form such as overlay and the form. And clear the input-fields.
        """
        self.hide()
        self._overlay.hideOverlay()
        self._firstname_field.clear()
        self._lastname_field.clear()
        self._role_dropdown.setCurrentIndex(0)


    """
    BACKEND
    """
    @staticmethod
    def __validateData(data) -> bool:
        for key, value in data.items():
            if value.strip() == "" or value is None:
                # prompt user that field must be filled.
                QMessageBox.warning(None, 'Warning', f"Field '{key}' is empty!")
                return False
            if value.lower() == 'select role':
                # prompt user to select a role
                QMessageBox.warning(None, 'Warning', f"Select a role")
                return False

        return True # return True if there are no anomalies

    def _submit(self, controller):
        data = self.__get_user_input

        if not self.__validateData(data):
            # if data is invalid, immediately return
            return
        QMessageBox.information(self, 'Notice', "Submitting data\nPress OK to continue")
        controller.submitUserdata(data) # send to database
        self.__closeForm() # close form after submission
        self._overlay.refresh('users') # reload table
        QMessageBox.information(self, 'Notice', "Successfully submitted the data\nTable is refreshed!")