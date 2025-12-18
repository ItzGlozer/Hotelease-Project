from PyQt6.QtCharts import QPieSeries, QChart, QChartView
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainter

from src.model.equipment_repository import EquipmentRepository
from src.model.user_data import UserData
from src.resource.builder import Build


class DashboardAdmin(QWidget):
    __STYLES = """
    QLabel#title {font-size: 40px; max-height: 40px;}
    
    """

    def __init__(self):
        super().__init__()

        # title
        title = Build.widget(QLabel, 'title', "Dashboard")

        # contents
        profile_frame = self._buildProfile()
        chart_frame = self._buildPieChart()
        layout = Build.flex(profile_frame, chart_frame)
        layout.setContentsMargins(50, 0, 50, 0)
        layout.setSpacing(50)


        # layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addLayout(layout)


        self.setStyleSheet(self.__STYLES)


    """
    WRAPPER
    """
    def _buildPieChart(self) -> QFrame:
        self.series = QPieSeries()
        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle('Equipment Stocks')
        chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        legend = chart.legend()
        legend.setAlignment(Qt.AlignmentFlag.AlignRight)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Chart Frame
        frame = QFrame()
        frame.setMaximumSize(500, 400)
        layout = QVBoxLayout(frame)
        layout.addWidget(chart_view)

        return frame


    def _buildProfile(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("""
        QFrame {background: #7a7ad5;}
        QLabel#h3 {font-size: 16px; max-height: 16px;}
        QLabel#h1 {font-size: 24px; max-height: 24px;}
        QLabel#h2 {font-size: 18px; max-height: 18px;}
        """)
        frame.setMaximumHeight(300)

        # labels
        lbl = Build.widget(QLabel, 'h1', "Profile")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        id_lbl = Build.widget(QLabel, 'h3', f"ID no. {UserData.user_id}")
        id_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl = Build.widget(QLabel, 'h1', f"{UserData.lastname}, {UserData.firstname}")
        role_lbl = Build.widget(QLabel, 'h2', f"{UserData.role}")
        role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = Build.flex(lbl, 'stretch', id_lbl,
                    name_lbl, role_lbl, 'stretch',
                    parent=frame, direction='column', alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 20, 0, 20)

        return frame

    """
    UTILITY
    """
    def default(self):
        ...

    def preload(self):
        self._loadEquipmentData()



    """
    BACKEND
    """

    def _loadEquipmentData(self):
        items = EquipmentRepository.fetchAll()
        for item in items:
            quantity = item.get('quantity', 0)
            if quantity is None:
                quantity = 0.0  # Ensure it's a float (not None)

            self.series.append(item['name'], float(quantity))

        for slice in self.series.slices():
            # Set the label with both name and percentage
            slice.setLabel(f"{slice.label()} ({slice.percentage() * 100:.2f}%)")

