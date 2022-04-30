import math
from PySide6 import QtCore, QtWidgets, QtGui
from utils.extra_math import *
from utils.drawing import *

class Gauge:
    def __init__(self, cx:int, cy:int, lower_val:int=0, upper_val:int=100, display_precision:int=0, display_description:str="", display_unit:str="", size=150, hint_range=5):
        self.theta = 0
        self.lower_theta = 225/180*3.1415
        self.upper_theta = -45/180*3.1415
        self.delta_theta = self.upper_theta - self.lower_theta
        self.cx = cx
        self.cy = cy
        self.lower_val = lower_val
        self.upper_val = upper_val
        self.delta_val = self.upper_val - self.lower_val
        self.value = 0
        self.display_precision = display_precision
        self.display_unit = display_unit

        self.display_description = display_description
        self.display_description_font = QtGui.QFont()
        self.display_description_font.setPixelSize(18)
        self.display_description_font.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, 2)

        self.display_value_font = QtGui.QFont()
        self.display_value_font.setPixelSize(25)
        self.display_value_font.setBold(True)

        self.display_hintvalues_font = QtGui.QFont()
        self.display_hintvalues_font.setPixelSize(18)
        self.display_hintvalues_font.setBold(True)
        self.display_hintvalues_font.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, 1)
        self.size = size

        self.hints = []
        self.hint_range = hint_range
        hint_values = [self.lower_val]
        for i in range(self.hint_range-2): hint_values += ["{:.0f}".format(self.lower_val + self.delta_val/(self.hint_range-1)* (i+1))]
        hint_values += [self.upper_val]
        for i, value in enumerate(hint_values):
            theta = self.lower_theta + self.delta_theta/(self.hint_range-1) * (i)
            (x,y) = point_at_angle(self.cx, self.cy, theta, self.size)
            self.hints += [(x,y,value)]

    def update_value(self, value):
        self.value = value

        if value < self.lower_val: value = self.lower_val
        elif value > self.upper_val: value = self.upper_val

        self.theta = (value-self.lower_val)/self.delta_val*self.delta_theta+self.lower_theta

    def draw(self, painter):
        self.update_value(self.value + 0.1)

        length = self.size

        from_x = self.cx
        from_y = self.cy
        to_x = math.cos(self.theta)*length+self.cx
        to_y = -math.sin(self.theta)*length+self.cy

        self.__draw_hints(painter)

        draw_arc(painter, self.cx, self.cy, length+20, -45, 270, width=1)
        draw_rounded_line(painter, QtCore.QPoint(from_x,from_y), QtCore.QPoint(to_x, to_y), width=7)
        painter.setFont(self.display_value_font)
        painter.drawText(self.cx-length, self.cy+length*0.4, length*2, 100, 0x0004, "{:.{}f}".format(self.value, self.display_precision) + self.display_unit)
        painter.setFont(self.display_description_font)
        painter.drawText(self.cx-length, self.cy+length*0.2, length*2, 100, 0x0004, self.display_description)

    def __draw_hints(self, painter):
        hintvalues_distance = self.size/2
        painter.setFont(self.display_hintvalues_font)
        painter.setPen(QtGui.qRgb(200, 200, 200))

        for (x,y,value) in self.hints:
            painter.drawText(x-25,y-25, 50, 50, 0x0084, str(value))