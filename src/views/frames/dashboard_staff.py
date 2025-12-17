from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame


class DashboardStaff(QWidget):
    __STYLES = """
    border: 2px solid black;
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(self.__STYLES)

        # table




        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)



    def default(self):
        ...

    def preload(self):
        ...