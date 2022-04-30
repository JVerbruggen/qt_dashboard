import sys
import math
import random
from PySide6 import QtCore, QtWidgets, QtGui
from components.gauge import Gauge

FPS = 60
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

class Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.setAutoFillBackground(True)
        self.setStyleSheet("* {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #444257, stop:1 #21202e);}")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/FPS)

        self.drawables = [
            Gauge(WINDOW_WIDTH/2 - 200,WINDOW_HEIGHT-200,0,200,0,display_description="SPEED",display_unit=" km/h"),
            Gauge(WINDOW_WIDTH/2 + 200,WINDOW_HEIGHT-200,0,60,1,display_description="MOTOR SPEED",display_unit=" rpm"),
            Gauge(WINDOW_WIDTH/2 - 150,WINDOW_HEIGHT-500,50,150,0,display_description="TEMP",size=75,hint_range=5)
        ]

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        
        for drawable in self.drawables:
            drawable.draw(qp)

        qp.end()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Dashboard()
    widget.setFixedSize(WINDOW_WIDTH,WINDOW_HEIGHT)
    widget.show()

    sys.exit(app.exec())