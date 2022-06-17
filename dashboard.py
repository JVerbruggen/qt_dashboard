import sys
from PySide6 import QtCore, QtWidgets, QtGui
from configuration.dashboard_config import DashboardConfig
from configuration.setup.demo_setup import DemoSetup
from configuration.setup.serial_setup import SerialSetup
from configuration.setup.setup import Setup
from dataclasses import dataclass
from utils.painter.qtpainter import HMIQtPainter
from utils.context.qt_context import HMIQtContext

WINDOW = (1600, 900)
FPS = 60
BACKGROUND_STYLE = "* {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #444257, stop:1 #21202e);}"

@dataclass
class DashboardPage:
    drawables: list["Drawable"]

class Dashboard(QtWidgets.QWidget):
    """
    Dashboard that fits in QT.
    Extends QWidget, where paintEvent is called by QT to update the widget.
    """

    def __init__(self, configuration: DashboardConfig):
        super().__init__()
        self.configuration = configuration
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setAutoFillBackground(True)
        self.setStyleSheet(BACKGROUND_STYLE)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.dashboard_update)
        self.timer.start(int(1000 / FPS))

    def dashboard_update(self):
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        painter = HMIQtPainter(qp)

        for drawable in self.configuration.get_drawables():
            drawable.draw(painter)

        qp.end()

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        pos = event.position()
        self.configuration.click_event(pos.x(), pos.y())

def get_setup() -> Setup:
    return DemoSetup()
    # return SerialSetup()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    cp = QtGui.QGuiApplication.screens()[-1].availableGeometry().center()
    

    setup = get_setup()
    context = HMIQtContext()

    widget = Dashboard(setup.create(context, WINDOW))
    # widget.setFixedSize(WINDOW[0], WINDOW[1])
    widget.setMouseTracking(True)
    widget.setGeometry(cp.x()-WINDOW[0]/2, cp.y()-WINDOW[1]/2, WINDOW[0], WINDOW[1])
    # enable touch controls here
    widget.show()
    # widget.showFullScreen()


    sys.exit(app.exec())
