import sys
from PySide6 import QtCore, QtWidgets, QtGui
from configuration.demo_dashboard_config import DemoDashboardConfig
from configuration.setup.demo_setup import DemoSetup
from configuration.setup.serial_setup import SerialSetup
from components.drawable.page_selector import PageSelectorFactory
from dataclasses import dataclass

WINDOW = (1600, 900)
FPS = 60
BACKGROUND_STYLE = "* {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #444257, stop:1 #21202e);}"

PAGE_IDEN_MAIN = "main"
PAGE_IDEN_MSG = "messages"

@dataclass
class DashboardPage:
    drawables: list["Drawable"]

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

        self.pages = {
            PAGE_IDEN_MAIN: DashboardPage(configuration.get_drawables(WINDOW)),
            PAGE_IDEN_MSG: DashboardPage([]),
        }
        self.selected_page_iden = PAGE_IDEN_MAIN
        self.selected_page = self.pages[self.selected_page_iden]

        self.page_selector = PageSelectorFactory.from_settings({
            "Main": PAGE_IDEN_MAIN,
            "Messages": PAGE_IDEN_MSG,
            })

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.dashboard_update)
        self.timer.start(int(1000 / FPS))

    def select_page(self, iden: str):
        self.selected_page_iden = iden
        self.selected_page = self.pages[self.selected_page_iden]

    def dashboard_update(self):
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)

        for drawable in self.selected_page.drawables:
            drawable.draw(qp)

        self.page_selector.draw(qp)

        qp.end()

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        pos = event.pos()

        hit_button = self.page_selector.hits(pos.x(), pos.y())
        if hit_button is None: return

        print("HIT", hit_button.iden)
        self.select_page(hit_button.iden)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    setup = DemoSetup()
    # setup = SerialSetup()
    widget = Dashboard(setup.create())
    widget.setFixedSize(WINDOW[0], WINDOW[1])
    widget.setMouseTracking(True)
    # enable touch controls here
    widget.show()

    sys.exit(app.exec())
