from utils.colors import Colors
from utils.extra_math import *
from utils.drawing import *
from components.drawable.drawable import Drawable
from components.variable.watchable_variable import WatchableRangeVariable
from utils.painter.painter import Painter


class Gauge(Drawable):
    """
    A gauge that listens to a variable and displays its value.
    """

    UPPER_DEG = 225
    LOWER_DEG = -45

    LOWER_THETA = UPPER_DEG / 180 * 3.1415
    UPPER_THETA = LOWER_DEG / 180 * 3.1415
    DELTA_THETA = UPPER_THETA - LOWER_THETA

    STRUCTURE_DRAW_WEIGHT = 3
    ROD_DRAW_WEIGHT = 7

    def __init__(self,
                 watching_variable: WatchableRangeVariable,
                 cx: int,
                 cy: int,
                 display_precision: int = 0,
                 display_description: str = "",
                 display_unit: str = "",
                 size=150,
                 hint_range=5):

        self.watching_variable = watching_variable
        self.theta = 0
        self.cx = cx
        self.cy = cy
        self.lower_val = watching_variable.get_lower_value()
        self.upper_val = watching_variable.get_upper_value()
        self.delta_val = self.upper_val - self.lower_val
        self.value = self.lower_val
        self.display_precision = display_precision
        self.display_unit = display_unit
        self.display_description = display_description
        self.size = size
        self.hints = []
        self.hint_range = hint_range

        self.__prepare_hints()
        self.__prepare_visuals()

    def __prepare_visuals(self):
        self.display_description_font = "GaugeLG"
        self.display_value_font = "GaugeMD"
        self.display_hintvalues_font = "GaugeSM"

    def __prepare_hints(self):
        hint_values = [self.lower_val]
        for i in range(self.hint_range - 2): hint_values += [
            "{:.0f}".format(self.lower_val + self.delta_val / (self.hint_range - 1) * (i + 1))]

        hint_values += [self.upper_val]

        for i, value in enumerate(hint_values):
            theta = self.LOWER_THETA + self.DELTA_THETA / (self.hint_range - 1) * (i)
            (x, y) = point_at_angle(self.cx, self.cy, theta, self.size)
            self.hints += [(x, y, value)]

    def update_value(self, value):
        self.value = value

        if value < self.lower_val:
            value = self.lower_val
        elif value > self.upper_val:
            value = self.upper_val

        self.theta = (value - self.lower_val) / self.delta_val * self.DELTA_THETA + self.LOWER_THETA

    def draw(self, painter: Painter):
        self.update_value(self.watching_variable.get_value())

        self.__draw_hints(painter)
        self.__draw_structure(painter)
        self.__draw_rod(painter)
        self.__draw_info(painter)

    def __draw_structure(self, painter: Painter):
        painter.draw_arc(self.cx, self.cy, self.size + 20, self.LOWER_DEG, self.UPPER_DEG - self.LOWER_DEG,
                         Colors.DEFAULT_LINE, width=self.STRUCTURE_DRAW_WEIGHT)

    def __draw_rod(self, painter: Painter):
        from_x = self.cx
        from_y = self.cy
        to_x = math.cos(self.theta) * self.size + self.cx
        to_y = -math.sin(self.theta) * self.size + self.cy
        painter.draw_rounded_line(from_x, from_y, int(to_x), int(to_y), Colors.DEFAULT_LINE, width=self.ROD_DRAW_WEIGHT)

    def __draw_hints(self, painter: Painter):
        hintvalues_distance = self.size / 2

        for (x, y, value) in self.hints:
            painter.draw_text_at(x - 25, y - 25, 50, 50, Colors.DEFAULT_LINE, str(value), self.display_hintvalues_font)
            # painter.drawText(x - 25, y - 25, 50, 50, 0x0084, str(value))

    def __draw_info(self, painter: Painter):
        painter.draw_text_at(self.cx - self.size, int(self.cy + self.size * 0.4), self.size * 2, 100,
                             (200, 200, 200, 255),
                             "{:.{}f} ".format(self.value, self.display_precision) + self.display_unit,
                             self.display_value_font)
        painter.draw_text_at(self.cx - self.size, int(self.cy + self.size * 0.4 - 25), self.size * 2, 100,
                             (200, 200, 200, 255), self.display_description, self.display_description_font)
