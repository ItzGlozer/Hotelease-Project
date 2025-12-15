from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import time

from src.resource.builder import Build
from src.views.frames.dashboard import Dashboard
from src.views.frames.inventory import Inventory
from src.views.frames.request_manager import RequestManager
from src.views.frames.user_manager import UserManager


class MainContent(QFrame):
    def __init__(self):
        super().__init__()

        self._dashboard = Dashboard()
        self._inventory = Inventory()
        self._request_manager = RequestManager()
        self._user_manager = UserManager()

        self._frames = [self._dashboard, self._inventory, self._request_manager, self._user_manager]


        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._dashboard)
        main_layout.addWidget(self._inventory)
        main_layout.addWidget(self._request_manager)
        main_layout.addWidget(self._user_manager)


    def _hideAll(self):
        for frame in self._frames:
            frame.hide()


    def defaultState(self):
        self._inventory.default()
        self._user_manager.default()

        # hide all frames except dashboard
        self._hideAll()
        time.sleep(0.01)
        self._dashboard.show()
        # self._user_manager.show()


    def showFrame(self, frame_name: str):
        self._hideAll()
        time.sleep(0.01)
        match frame_name.lower():
            case 'dashboard':
                self._dashboard.show()
            case 'inventory':
                self._inventory.show()
            case 'manage user':
                self._user_manager.show()
            case 'manage request':
                self._request_manager.show()

















