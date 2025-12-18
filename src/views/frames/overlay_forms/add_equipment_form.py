from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel, QApplication, QVBoxLayout, QPushButton

from src.resource.builder import Build


class AddEquipmentForm(QWidget):

    __STYLES = """
    QLabel{font-size: 40px;}
    """
    def __init__(self, overlay):
        super().__init__()
        self._overlay = overlay

        #
        name_lbl, self._name_field = self.__buildInputField("Equipment Name:", "ex. Vacuum")
        name_layout = Build.flex(name_lbl, self._name_field, direction="column")

        # buttons
        self._submit_btn = QPushButton("Submit")
        self._cancel_btn = QPushButton("Cancel")
        button_layout = Build.flex(self._submit_btn, self._cancel_btn)


        # layout
        main_layout = Build.flex(name_layout, button_layout,
                                 direction="column", parent=self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        main_layout.setSpacing(12)

        self.setStyleSheet(self.__STYLES)


    """
    UTILITY
    """
    @property
    def __get_input_data(self) -> dict:
        name = self._name_field.text()
        self.__closeForm()
        return {"name": name}

    def connectSignals(self, controller):
        self._submit_btn.clicked.connect(lambda _: self._submit(controller))
        self._cancel_btn.clicked.connect(self.__closeForm)

    """
    FRONTEND
    """
    def showForm(self):
        self.show()

    def default(self):
        self.hide()

    def __closeForm(self):
        """
        Hide the form such as overlay and the form. And clear the input-fields.
        """
        self.hide()
        self._overlay.hideOverlay()
        self._name_field.clear()



    """
    BACKEND
    """
    def _submit(self, controller):
        data = self.__get_input_data
        controller.submitEquipment(data) # send to database
        self._overlay.refresh('inventory') # refresh table



    """
    WRAPPER
    """
    @staticmethod
    def __buildInputField(text, placeholder) -> tuple:
        label = Build.widget(QLabel, text=text)
        label.setStyleSheet("font-size: 18px;")
        text_field = Build.widget(QLineEdit, placeholder=placeholder)
        text_field.setStyleSheet("""
        font-size: 18px;
        background: #8f8fd6;
        border: 1px solid black;
        border-radius: 4px;
        padding: 2 0 2 10;
        """)
        return label, text_field




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AddEquipmentForm()
    window.show()
    sys.exit(app.exec())