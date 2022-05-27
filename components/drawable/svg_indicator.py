from components.drawable.drawable import Drawable
from PySide6 import QtGui

from components.variable.watchable_variable import WatchableVariable


class SvgIndicator(Drawable):
    """
    An indicater depicted by a SVG icon that listens to a variable and displays its value (on or off).
    """

    BLACK = QtGui.QColor.fromRgb(0, 0, 0, 255)
    RED = QtGui.QColor.fromRgb(232, 38, 49, 255)
    GREEN = QtGui.QColor.fromRgb(151, 191, 78, 255)
    ORANGE = QtGui.QColor.fromRgb(255, 193, 14, 255)

    def __init__(self, svg_filepath, watchable_variable: WatchableVariable, on_color: QtGui.QColor, x: int, y: int,
                 size: int):
        self.svg_filepath = svg_filepath
        self.watchable_variable = watchable_variable
        self.on_color = on_color
        self.x = x
        self.y = y
        self.size = size
        self.old_state = -1

        self.img = QtGui.QPixmap(self.svg_filepath)
        qp = QtGui.QPainter(self.img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        qp.fillRect(self.img.rect(), on_color)
        qp.end()

        self.blink_state = False

    def set_color(self, new_state: int):
        self.blink_state = not self.blink_state

        qp = QtGui.QPainter(self.img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)

        qp.fillRect(self.img.rect(), self.on_color if new_state else SvgIndicator.BLACK)

        qp.end()

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

    def __init__(self, svg_filepath, watchable_variable: WatchableVariable, on_color: QtGui.QColor, x: int, y: int,
            size: int, interval: int):
        super().__init__(svg_filepath, watchable_variable, on_color, x, y, size)

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
