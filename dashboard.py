import sys

import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QScreen

from configuration.demo_dashboard_config import DemoDashboardConfig
from configuration.setup.demo_setup import DemoSetup
from configuration.setup.serial_setup import SerialSetup

WINDOW = (1600, 900)
FPS = 60
BACKGROUND_STYLE = "* {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #444257, stop:1 #21202e);}"


class Dashboard(QtWidgets.QWidget):
    """
    Dashboard that fits in QT.
    Extends QWidget, where paintEvent is called by QT to update the widget.
    """

    def __init__(self, configuration):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setAutoFillBackground(True)
        self.setStyleSheet(BACKGROUND_STYLE)

        self.drawables = configuration.get_drawables(WINDOW)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.dashboard_update)
        self.timer.start(int(1000 / FPS))

    def dashboard_update(self):
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)

        for drawable in self.drawables:
            drawable.draw(qp)

        qp.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    setup = DemoSetup()
    # setup = SerialSetup()
    widget = Dashboard(setup.create())
    widget.setFixedSize(WINDOW[0], WINDOW[1])
    widget.show()
    widget.setGeometry(app.screens()[1].availableGeometry())

    sys.exit(app.exec())
