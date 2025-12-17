from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from src.model.user_data import UserData
from src.resource.builder import Build


class AddRequestForm(QWidget):

    __equipment_selected = None

    def __init__(self, overlay):
        super().__init__()
        self._overlay = overlay

        #
        self._id_lbl = QLabel("ID")

        # NAME text-field
        name_lbl, self._name_field = self.__buildInputField(QLineEdit, "Equipment Name:", "disabled")
        self._name_field.setEnabled(False)
        name_layout = Build.flex(name_lbl, self._name_field, direction="column")

        # Stock type dropdown
        items = ["Stock in", "Stock out"]
        entry_lbl, self._entry_dropdown = self.__buildInputField(QComboBox, "Entry Type:", items=items)
        entry_layout = Build.flex(entry_lbl, self._entry_dropdown, direction="column")

        # Quantity Field
        quantity_lbl, self._quantity_field = self.__buildInputField(QLineEdit, "Quantity: ", "ex. 100")
        quantity_lbl.setStyleSheet("font-size: 14px;")
        self._quantity_field.setMaximumHeight(24)
        quantity_layout = Build.flex(quantity_lbl, self._quantity_field, alignment=Qt.AlignmentFlag.AlignHCenter)

        # buttons
        self._submit_btn = QPushButton("Submit")
        self._cancel_btn = QPushButton("Cancel")
        button_layout = Build.flex(self._submit_btn, self._cancel_btn)


        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self._id_lbl)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(entry_layout)
        main_layout.addLayout(quantity_layout)
        main_layout.addLayout(button_layout)



    """
    WRAPPER
    """
    @staticmethod
    def __buildInputField(input_type, text, placeholder=None, items=None) -> tuple:
        label = Build.widget(QLabel, text=text)
        label.setStyleSheet("font-size: 18px;")
        input_widget = Build.widget(input_type, placeholder=placeholder, items=items)
        input_widget.setStyleSheet(f"""
                {'color: black;' if placeholder == 'disabled' else ''}
                font-size: 16px;
                background: #8f8fd6;
                border: 1px solid black;
                border-radius: 4px;
                padding: 2 0 2 10;
                """)
        return label, input_widget

    @staticmethod
    def __validateData(data) -> bool:
        try:
            int(data)
            return True
        except ValueError:
            return False


    @property
    def __get_input_data(self) -> dict | None:
        item_id = self._id_lbl.text()
        # name = self._name_field.text() # deprecated
        entry_type = self._entry_dropdown.currentText()
        quantity = self._quantity_field.text()

        if self.__validateData(quantity):
            data = {
                "user_id": UserData.user_id,
                "item_id": item_id,
                "type": entry_type,
                "quantity": quantity
            }
            return data
        else:
            return None



    """
    FRONTEND
    """
    def default(self):
        self.hide()

    def connectSignals(self, controller):
        self._submit_btn.clicked.connect(lambda _: self._submit(controller))
        self._cancel_btn.clicked.connect(self.__closeForm)

    def showForm(self, pre_data: dict=None):
        self.show()
        if pre_data:
            self.__equipment_selected = pre_data
            self._id_lbl.setText(pre_data["id"])
            self._name_field.setText(pre_data["name"])
            self._quantity_field.setText(pre_data["quantity"])

    def __closeForm(self):
        """
        Hide the form such as overlay and the form. And clear the input-fields.
        """
        self.hide()
        self._overlay.hideOverlay()
        self._quantity_field.clear()
        self._name_field.clear()


    """
    BACKEND
    """
    def _submit(self, controller):
        data = self.__get_input_data
        if data:
            controller.submitRequest(data)
            self._overlay.refresh("request")
            self.__closeForm()
        else:
            QMessageBox.warning(None, "Notice", "Invalid input!\nQuantity must be a whole number.")



























