from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from src.model.user_data import UserData
from src.resource.builder import Build


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        user = UserData()

        # title
        title = QLabel(f"Welcome {user.firstname if user.firstname else 'Hecker'}!")
        title.setStyleSheet("font-size: 34px; max-height: 100px;")

        """
        COUNTS
        """
        self._item_lbl = self.__createCardCount("Total Items:")
        self._low_stock_lbl = self.__createCardCount("Low Stock Count:")
        self._pending_request_lbl = self.__createCardCount("Pending Requests:")
        count_layout = Build.flex(self._item_lbl, self._low_stock_lbl, self._pending_request_lbl)

        """
        SCOOP
        """
        # STOCKS ALERT SECTION
        # items
        self.stock_alert_item1 = self.__createScoopItem("Equipment #1")
        self.stock_alert_item2 = self.__createScoopItem("Equipment #2")
        # frame
        stock_alert_frame = self.__createScoopFrame(self.stock_alert_item1, self.stock_alert_item2,
                                                    title="Low Stock alerts")

        # RECENT REQUEST SECTION
        # items
        self.request_item1 = self.__createScoopItem("Request #1")
        self.request_item2 = self.__createScoopItem("Request #2")
        # frame
        request_frame = self.__createScoopFrame(self.request_item1, self.request_item2, title="Recent Request")

        # SCOOP LAYOUT
        scoop_layout = Build.flex(stock_alert_frame, request_frame)

        """
        Main Layout
        """
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(count_layout)
        layout.addLayout(scoop_layout)


    """
    UTILITY
    """

    def __createCardCount(self, text) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""QLabel { 
                background: #8f8fd6; 
                max-width: 200px; 
                max-height: 150px; 
                border-radius: 14px;
                font-size: 14px; 
                }""")
        return label

    def __createScoopFrame(self, *items, title="Set title") -> QFrame:
        # label
        label = QLabel(title)
        label.setStyleSheet("""QLabel { 
                font-size: 30px; 
                max-height: 40px; 
                border-radius: 14px;
                }""")

        frame = QFrame()
        frame.setObjectName('frame')
        frame.setStyleSheet("QFrame#frame {border: 3px solid black; max-height: 370px; }")
        layout = Build.flex(label, *items, direction="column")
        frame.setLayout(layout)

        return frame

    def __createScoopItem(self, text: str) -> QPushButton:
        button = QPushButton(text)
        button.setStyleSheet("""
                QPushButton {
                border: 3px solid black;
                border-radius: 14px;
                max-height: 100px;
                }""")
        return button

    """
    EVENTS
    """

    def __updateLabelCount(self, label, count):
        text = label.text()
        index = text.find(':')
        label.setText(f"{text[:index + 1]} {count}")

    def updateTotalItems(self, count):
        self.__updateLabelCount(self._item_lbl, count)

    def updateLowStocks(self, count):
        self.__updateLabelCount(self._low_stock_lbl, count)

    def updatePendingRequests(self, count):
        self.__updateLabelCount(self._pending_request_lbl, count)