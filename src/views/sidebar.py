from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QFrame
from src.resource.builder import Build
from src.views.frames.logout import Logout


class Sidebar(QFrame):
    __BUTTON_STYLES = """
        font-size: 14px;
        background: #8f8fd6;
        color: white;
        border: 2px solid black;
        border-radius: 9px;
        width: 150px;
        height: 50px;
    """

    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window

        self.setMaximumWidth(int(self._main_window.width()*0.3))

        # widgets
        self._dashboard = None
        self._inventory = None
        self._manage_user = None
        self._manage_request = None
        self._generate_reports = None
        self._logout = None

        # layout
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.setSpacing(50)


        # init
        buttons = [self._dashboard, self._inventory, self._manage_user, self._manage_request, self._generate_reports,
                   self._logout]
        self._initButtons(buttons)


    def _initButtons(self, buttons: list):
        print("execute")
        headers = ["Dashboard", "Inventory", "Manage User", "Manage Request", "Generate Reports", "Logout"]
        for i, button in enumerate(buttons):
            button: QPushButton = Build.widget(QPushButton, text=headers[i])
            button.setStyleSheet(Sidebar.__BUTTON_STYLES)
            self._layout.addWidget(button)
            self.connectSignals(button, headers[i])


    def connectSignals(self, button, name):
        if name.lower() == "logout":
            self._initLogout(button)
        else:
            show = self._main_window.showMainContentFrame
            button.clicked.connect(lambda e: show(name))


    def _initLogout(self, button):
        self._logout = Logout(self._main_window)
        button.clicked.connect(self._logout.logout)


