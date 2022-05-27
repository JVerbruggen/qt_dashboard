from components.drawable.drawable import Drawable
from PySide6 import QtGui

from components.variable.watchable_variable import WatchableVariable
from utils.colors import Colors
import utils.drawing

class SvgIndicator(Drawable):
    """
    An indicater depicted by a SVG icon that listens to a variable and displays its value (on or off).
    """
    def __init__(self, svg_filepath: str, watchable_variable: WatchableVariable, x: int, y: int, size: int=10, 
            on_color: QtGui.QColor = Colors.GREEN):
        self.svg_filepath = svg_filepath
        self.watchable_variable = watchable_variable
        self.on_color = on_color
        self.x = x
        self.y = y
        self.size = size
        self.old_state = -1

        self.img = QtGui.QPixmap(self.svg_filepath)
        utils.drawing.fill_svg(self.img, self.on_color)

        self.blink_state = False

    def set_color(self, new_state: int):
        self.blink_state = not self.blink_state
        utils.drawing.fill_svg(self.img, self.on_color if new_state else Colors.BLACK)

    def draw(self, painter: QtGui.QPainter):
        current_state = self.watchable_variable.get_value()

        if current_state != self.old_state:
            self.set_color(current_state)

        painter.drawPixmap(int(self.x - self.size / 2), int(self.y - self.size / 2), self.size, self.size, self.img)


class SvgBlinker(SvgIndicator):
    """
    An indicater depicted by a SVG icon that listens to a variable.
    Blinks if value is 1, goes to off color if 0
    """

    def __init__(self, svg_filepath: str, watchable_variable: WatchableVariable, x: int, y: int, size: int=10, interval: int=30,
            on_color: QtGui.QColor = Colors.GREEN):
        super().__init__(svg_filepath, watchable_variable, x, y, size, on_color)

        self.interval_state = interval
        self.interval = interval
        self.blink_phase = True
        self.blinking = False

    def update_interval(self):
        self.interval_state -= 1
        if self.interval_state <= 0:
            self.blink_phase = not self.blink_phase
            self.interval_state = self.interval

    def set_color(self, new_state: int):
        if new_state == 1:
            if not self.blinking:
                self.blinking = True
                self.interval_state = self.interval

            self.update_interval()
            
        elif self.blinking: self.blinking = False

        blink_state = int(self.blink_phase)
        super().set_color(blink_state)