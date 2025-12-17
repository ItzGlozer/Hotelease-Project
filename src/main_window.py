from PyQt6.QtWidgets import QApplication

from src.controller import Controller
from src.model.user_data import UserData
from src.views.main_content import MainContent
from src.views.window import Window
from src.views.sidebar import Sidebar
from src.views.titlebar import TitleBar

class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self._controller = None
        self.setStyleSheet("* {font-family: Times New Roman;}")

        # widgets
        self.titlebar = TitleBar()
        self.sidebar = Sidebar(self)
        self.main_content = MainContent()

        self.initUi()

        # state
        self.main_content.default()
        # self.main_content.pre_load()



    def initUi(self):
        self.theThreeHorsemen(self.titlebar, self.sidebar, self.main_content)


    """
    EVENTS
    """
    def showMainContentFrame(self, frame_name):
        self.main_content.showFrame(frame_name)

    def refreshMainContent(self, frame_name):
        self.main_content.refresh(frame_name)

    """
    BACKEND
    """
    def setController(self, controller):
        self._controller = controller
        self.main_content.connectSignal(controller)






if __name__ == '__main__':
    import sys
    from src.app import App
    from src.controller import Controller
    q_app = QApplication(sys.argv)
    credentials = {
        "id": 2,
        "firstname": "Glych",
        "lastname": "Final Boss",
        "role": "admin",
    }
    UserData(credentials)
    view = MainWindow()
    view.show()

    app = App
    controller = Controller(view, app)
    view.setController(controller)

    sys.exit(q_app.exec())

