from PyQt6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from src.views.frames.overlay_forms.add_equipment_form import AddEquipmentForm
from src.views.frames.overlay_forms.add_request_form import AddRequestForm


class Overlay(QFrame):
    __STYLES = """
    background: #7a7ad5; 
    /* border: 2px solid black; */
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.setStyleSheet(Overlay.__STYLES)
        self.setGeometry(312, 171, 300, 250)

        self._add_equipment_form = AddEquipmentForm(self)
        self._add_request_form = AddRequestForm(self)


        # layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._add_equipment_form)
        main_layout.addWidget(self._add_request_form)


    def connectSignals(self, controller):
        self._add_equipment_form.connectSignals(controller)
        self._add_request_form.connectSignals(controller)

    def default(self):
        self.hideOverlay()
        self._add_equipment_form.default()
        self._add_request_form.default()

    def hideOverlay(self):
        self.hide()

    def showForm(self, form_name, pre_data=None):
        self.show()
        match form_name:
            case "add equipment":
                self._add_equipment_form.show()
            case "add request":
                self._add_request_form.showForm(pre_data)

    def refresh(self, frame_name):
        self._parent.refresh(frame_name)
