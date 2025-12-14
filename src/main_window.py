from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton

from src.views.main_content import MainContent
from src.views.window import Window
from src.views.sidebar import Sidebar
from src.views.titlebar import TitleBar

class MainWindow(Window):
    def __init__(self, credentials: dict):
        super().__init__()
        self.setStyleSheet("* {font-family: Times New Roman;}")

        # widgets
        self.titlebar = TitleBar()
        self.sidebar = Sidebar(self, credentials)
        self.main_content = MainContent(credentials)


        self.initUi()

        # state
        self.main_content.defaultState()

        # self.proxyEquipmentData()


    def initUi(self):
        self.theThreeHorsemen(self.titlebar, self.sidebar, self.main_content)


    """
    EVENTS
    """
    def showMainContentFrame(self, frame_name):
        self.main_content.showFrame(frame_name)


    def proxyEquipmentData(self):
        data = [
            (1, "equipment 1", 11, "In Stock", "Action"),
            (2, "equipment 2", 21, "In Stock", "Action"),
            (3, "equipment 3", 31, "In Stock", "Action"),
            (4, "equipment 4", 41, "In Stock", "Action"),
        ]

        for item in data:
            self.main_content.appendData(item)

