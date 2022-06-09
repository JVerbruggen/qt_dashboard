from components.drawable.drawable import Drawable
from utils.drawing import *
from utils.extra_math import point_at_angle


class BarDisplay(Drawable):
    HINT_FONT_SIZE = 18
    VALUE_FONT_SIZE = 25
    DESC_FONT_SIZE = 15

    def __init__(self,
                 watching_variable: WatchableRangeVariable,
                 cx: int,
                 cy: int,
                 width: int,
                 height: int,
                 display_precision: int = 0,
                 display_description: str = "",
                 display_unit: str = "",
                 size=150,
                 hint_range=5):

        self.watching_variable = watching_variable
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.display_precision = display_precision
        self.display_description = display_description
        self.display_unit = display_unit
        self.lower_val = watching_variable.get_lower_value()
        self.upper_val = watching_variable.get_upper_value()
        self.delta_val = self.upper_val - self.lower_val
        self.value = self.lower_val
        self.size = size
        self.hints = []
        self.hint_range = hint_range

        self.__prepare_hints()
        self.__prepare_visuals()

    def __prepare_visuals(self):
        self.display_description_font = QtGui.QFont()
        self.display_description_font.setPixelSize(self.DESC_FONT_SIZE)

        self.display_value_font = QtGui.QFont()
        self.display_value_font.setPixelSize(self.VALUE_FONT_SIZE)
        self.display_value_font.setBold(True)

        self.display_hintvalues_font = QtGui.QFont()
        self.display_hintvalues_font.setPixelSize(self.HINT_FONT_SIZE)
        self.display_hintvalues_font.setBold(True)
        self.display_hintvalues_font.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, 1)

    def __prepare_hints(self):
        hint_values = [self.lower_val]
        for i in range(self.hint_range - 2): hint_values += [
            "{:.0f}".format(self.lower_val + self.delta_val / (self.hint_range - 1) * (i + 1))]

        hint_values += [self.upper_val]

        for i, value in enumerate(hint_values):
            (x, y) = point_at_angle(self.cx, self.cy, 100, self.size)
            self.hints += [(x, y, value)]

    def update_value(self, value):
        self.value = value

    def draw(self, painter: QtGui.QPainter):
        self.update_value(self.watching_variable.get_value())

        self.__draw_hints(painter)
        self.__draw_structure(painter)
        self.__fill_structure(painter)
        self.__draw_info(painter)

    def __draw_structure(self, painter):
        draw_rect(painter, self.cx, self.cy, self.width, self.height)

    def __fill_structure(self, painter):
        fill_rect(painter, self.cx, self.cy, self.width, self.height, self.watching_variable)

    def __draw_hints(self, painter):
        painter.setFont(self.display_hintvalues_font)
        painter.setPen(QtGui.qRgb(200, 200, 200))

        for (x, y, value) in self.hints:
            painter.drawText(x, y, 50, 50, 0x0084, str(value))

    def __draw_info(self, painter):
        draw_text_at(painter, self.cx, self.cy - 55, self.width, self.height,
                     self.display_description, self.display_description_font)

        draw_text_at(painter, self.cx, self.cy - 35, self.width, self.height,
                     "{:.{}f} ".format(self.value, self.display_precision) + self.display_unit, self.display_value_font)