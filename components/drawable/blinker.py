from components.drawable.drawable import Drawable
from PySide6 import QtGui

from components.variable.watchable_variable import WatchableVariable


class SvgIndicator(Drawable):
    def __init__(self, svg_filepath, watchable_variable: WatchableVariable, on_color: QtGui.QColor, x: int, y: int,
                 size: int):
        self.svg_filepath = svg_filepath
        self.watchable_variable = watchable_variable
        self.on_color = on_color
        self.off_color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        self.x = x
        self.y = y
        self.size = size
        self.old_state = -1

        self.img = QtGui.QPixmap(self.svg_filepath)
        qp = QtGui.QPainter(self.img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        qp.fillRect(self.img.rect(), QtGui.QColor('blue'))
        qp.end()

        self.blink_state = False

    def set_color(self, new_state: int):
        self.blink_state = not self.blink_state

        qp = QtGui.QPainter(self.img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)

        qp.fillRect(self.img.rect(), self.on_color if new_state else self.off_color)

        qp.end()

    def draw(self, painter: QtGui.QPainter):
        current_state = self.watchable_variable.get_value()

        if current_state != self.old_state:
            self.set_color(current_state)

        painter.drawPixmap(int(self.x - self.size / 2), int(self.y - self.size / 2), self.size, self.size, self.img)

        painter.drawPoint(self.x, self.y)

        pass
