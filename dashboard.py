import sys
import math
import random
from PySide6 import QtCore, QtWidgets, QtGui
from components.gauge import Gauge

fps = 60
width = 1400
height = 800

class Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window, QtGui.qRgb(33, 32, 46))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/fps)

        self.drawables = [
            Gauge(width/2 - 200,height-200,0,200,0,display_description="SPEED",display_unit=" km/h"),
            Gauge(width/2 + 200,height-200,0,60,1,display_unit=" rpm"),
            Gauge(width/2 - 150,height-500,0,150,0,size=75,hint_range=4)
        ]

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        
        for drawable in self.drawables:
            drawable.draw(qp)

        qp.end()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Dashboard()
    widget.setFixedSize(width,height)
    widget.show()

    sys.exit(app.exec())