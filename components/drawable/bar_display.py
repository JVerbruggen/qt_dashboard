from PySide6 import QtGui

from components.drawable.drawable import Drawable
from components.variable.watchable_variable import WatchableRangeVariable
from utils.drawing import *

class BarDisplay(Drawable):
    def __init__(self,
                 watching_variable: WatchableRangeVariable,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 display_precision: int = 0,
                 display_description: str = "",
                 display_unit: str = "",
                 fill: int = 0):

        self.watching_variable = watching_variable
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display_precision = display_precision
        self.display_description = display_description
        self.display_unit = display_unit
        self.fill = fill
        self.lower_val = watching_variable.get_lower_value()
        self.upper_val = watching_variable.get_upper_value()

    def draw(self, painter: QtGui.QPainter):
        # self.update_value(self.watching_variable.get_value())

        # painter.drawRoundedRect(0, 0, 100, 100, 5, 5)
        # painter.drawRoundedRect

        draw_rect(painter, self.x, self.y, self.width, self.height)

        # self.__draw_structure(painter)
        # self.__draw_rod(painter)
        # self.__draw_info(painter)