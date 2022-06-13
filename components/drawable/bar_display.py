from components.drawable.drawable import Drawable
from components.variable.watchable_variable import WatchableRangeVariable
from utils.extra_math import point_at_angle
from utils.painter.painter import Painter


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

    def draw(self, painter: Painter):
        self.update_value(self.watching_variable.get_value())

        self.__draw_hints(painter)
        self.__draw_structure(painter)
        self.__fill_structure(painter)
        self.__draw_info(painter)

    def __draw_structure(self, painter):
        painter.draw_box(self.cx, self.cy, self.width, self.height, (200, 200, 200, 255))

    def __fill_structure(self, painter):
        fill_height = self.height / self.watching_variable.get_upper_value() * self.watching_variable.get_value()
        fill_height = self.height - fill_height + 2

        painter.draw_box_filled(self.cx + 1, self.cy + fill_height, self.width - 3, self.height - fill_height - 1, (200, 200, 200, 255))

    def __draw_hints(self, painter):
        for (x, y, value) in self.hints:
            painter.draw_text_at(x, y, 50, 50, (200, 200, 200, 255), str(value), "GaugeSM")

    def __draw_info(self, painter: Painter):
        painter.draw_text_at(self.cx, self.cy - 55, self.width, self.height, (200, 200, 200, 255),
                     self.display_description, "BarMD")

        painter.draw_text_at(self.cx, self.cy - 35, self.width, self.height, (200, 200, 200, 255),
                     "{:.{}f} ".format(self.value, self.display_precision) + self.display_unit, "BarMD")