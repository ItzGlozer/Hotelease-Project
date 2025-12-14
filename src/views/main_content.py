from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import time

from src.resource.builder import Build
from src.views.frames.dashboard import Dashboard
from src.views.frames.inventory import Inventory


class MainContent(QFrame):
    def __init__(self, credentials: dict):
        super().__init__()

        self._dashboard = Dashboard(credentials)
        self._inventory = Inventory()

        self._frames = [self._dashboard, self._inventory]


        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._dashboard)
        main_layout.addWidget(self._inventory)


    def _hideAll(self):
        for frame in self._frames:
            frame.hide()


    def defaultState(self):
        # hide all frames except dashboard
        self._hideAll()
        time.sleep(0.01)
        self._dashboard.show()


    def showFrame(self, frame_name: str):
        self._hideAll()
        time.sleep(0.01)
        match frame_name.lower():
            case 'dashboard':
                self._dashboard.show()
            case 'inventory':
                self._inventory.show()
















