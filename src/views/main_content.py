from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import time

from src.model.user_data import UserData
from src.resource.builder import Build
from src.views.frames.request_manager_staff import RequestManagerStaff
from src.views.frames.dashboard_admin import DashboardAdmin
from src.views.frames.dashboard_staff import DashboardStaff
from src.views.frames.inventory_admin import InventoryAdmin
from src.views.frames.inventory_staff import InventoryStaff
from src.views.frames.overlay import Overlay
from src.views.frames.request_manager_admin import RequestManagerAdmin
from src.views.frames.user_manager import UserManager


class MainContent(QFrame):

    def __init__(self):
        super().__init__()

        if UserData.is_admin:
            self._frames = self._admin_setup()
        else:
            self._frames = self._staff_setup()
        Build.flex(*self._frames, parent=self)

        self._overlay = Overlay(self)


    def _admin_setup(self) -> list:
        self._dashboard = DashboardAdmin()
        self._inventory = InventoryAdmin(self)
        self._request_manager = RequestManagerAdmin()
        self._user_manager = UserManager(self)
        return [self._dashboard, self._inventory, self._request_manager, self._user_manager]

    def _staff_setup(self) -> list:
        self._dashboard = DashboardStaff()
        self._inventory = InventoryStaff(self)
        self._request_manager = RequestManagerStaff(self)
        return [self._dashboard, self._inventory, self._request_manager]


    def _hideAll(self):
        for frame in self._frames:
            frame.hide()


    def connectSignals(self, controller):
        self._overlay.connectSignals(controller)
        self._request_manager.connectSignals(controller)
        self._inventory.connectSignals(controller)
        self._request_manager.connectSignals(controller)
        if UserData.is_admin:
            self._user_manager.connectSignals(controller)

    def default(self):
        self._dashboard.default()
        self._inventory.default()
        self._request_manager.default()
        self._overlay.default()
        if UserData.is_admin:
            self._user_manager.default()

        # hide all frames except dashboard
        self._hideAll()
        time.sleep(0.01)

        self._dashboard.show()


    def pre_load(self):
        self._dashboard.preload()
        self._inventory.preload()
        self._request_manager.preload()
        if UserData.is_admin:
            self._user_manager.preload()


    def showOverlay(self, form_name, pre_data=None):
        self._overlay.showForm(form_name, pre_data)

    def refresh(self, frame_name):
        match frame_name:
            case 'inventory':
                self._inventory.loadInventory()
            case 'request':
                self._request_manager.loadAllRequest()
            case 'users':
                self._user_manager.loadUsers()

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

















