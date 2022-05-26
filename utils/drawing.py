from PySide6 import QtCore, QtGui

"""
Drawing tools that weren't as easy with the default QT library
"""

def draw_rounded_line(painter: QtGui.QPainter, from_point: QtCore.QPoint, to_point: QtCore.QPoint, width: int = None):
    """
    Draws a line with rounded corners
    """
    if width:
        pen = QtGui.QPen(QtGui.Qt.white)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setWidth(width)
        painter.setPen(pen)

    painter.drawLine(QtCore.QLine(from_point, to_point))


def draw_arc(painter: QtGui.QPainter, cx: int, cy: int, rad: int, start_deg: int, length_deg: int, width: int = None):
    """
    Draws a part circle
    """
    if width:
        pen = QtGui.QPen(QtGui.Qt.white)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setColor(QtGui.qRgb(200, 200, 200))
        pen.setWidth(width)
        painter.setPen(pen)

    painter.drawArc(cx - rad, cy - rad, rad * 2, rad * 2, start_deg * 16, length_deg * 16)


def draw_text_at(painter: QtGui.QPainter, x: int, y: int, w: int, h: int, text: str, font: QtGui.QFont = None):
    """
    Draw text at given position and size
    """
    if font: painter.setFont(font)
    painter.drawText(x, y, w, h, 0x0004, text)
