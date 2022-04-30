import sys
import math
import random
from PySide6 import QtCore, QtWidgets, QtGui
from components.gauge import Gauge
from components.variable.demo_variables import *
from components.variable.canbus_variable import *

FPS = 60
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

class Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setAutoFillBackground(True)
        self.setStyleSheet("* {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #444257, stop:1 #21202e);}")

        self.variable_dummy = DemoStaticVariable(40, 0, 100)


        # self.variable_speed = DemoLoopingVariable(0, 0, 240, 0.25)
        self.variable_speed = CanbusVariable()
        # self.variable_speed = DemoStaticVariable(70, 0, 240)
        self.variable_motorspeed = DemoLoopingVariable(0, 0, 60)
        self.variable_temp = DemoLoopingVariable(50, 50, 240)

        self.drawables = [
            Gauge(self.variable_speed, WINDOW_WIDTH/2 - 200,WINDOW_HEIGHT-200,0,display_description="SPEED",display_unit=" km/h",hint_range=13),
            Gauge(self.variable_motorspeed, WINDOW_WIDTH/2 + 200,WINDOW_HEIGHT-200,1,display_description="MOTOR SPEED",display_unit=" rpm"),
            Gauge(self.variable_temp, WINDOW_WIDTH/2 - 150,WINDOW_HEIGHT-500,0,display_description="TEMP",size=75,hint_range=5),
            # dummys
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 - 400,WINDOW_HEIGHT-500,0,display_description="dummy",size=75,hint_range=5),
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 - 150,WINDOW_HEIGHT-700,0,display_description="dummy",size=75,hint_range=5),
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 - 400,WINDOW_HEIGHT-700,0,display_description="dummy",size=75,hint_range=5),
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 + 400,WINDOW_HEIGHT-500,0,display_description="dummy",size=75,hint_range=5),
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 + 400,WINDOW_HEIGHT-700,0,display_description="dummy",size=75,hint_range=5),
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 + 150,WINDOW_HEIGHT-500,0,display_description="dummy",size=75,hint_range=5),
            Gauge(self.variable_dummy, WINDOW_WIDTH/2 + 150,WINDOW_HEIGHT-700,0,display_description="dummy",size=75,hint_range=5),
        ]

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/FPS)

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