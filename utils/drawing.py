from PySide6 import QtCore, QtGui

"""
Drawing tools that weren't as easy with the default QT library
"""

DEFAULT_LINE_WIDTH = 2
DEFAULT_ROUNDED_WIDTH = 7
FONT_FAMILY = "Times"
FONT_MD = QtGui.QFont(FONT_FAMILY, 13)
FONT_SM = QtGui.QFont(FONT_FAMILY, 12)

def default_line_pen(color: QtGui.QColor = QtGui.QColor.fromRgb(200,200,200), width: int=DEFAULT_LINE_WIDTH):
    pen = QtGui.QPen(color)
    pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
    pen.setColor(color)
    pen.setWidth(width)
    return pen

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

def draw_box(painter: QtGui.QPainter, x: int, y: int, w: int, h: int):
    """
    Draws a rounded box
    """
    painter.drawRoundedRect(x, y, w, h, DEFAULT_ROUNDED_WIDTH, DEFAULT_ROUNDED_WIDTH)

def draw_box_filled(painter: QtGui.QPainter, x: int, y: int, w: int, h: int, color: QtGui.QColor, width: int=DEFAULT_LINE_WIDTH):
    """
    Draws a filled rounded box
    """
    path = QtGui.QPainterPath()
    path.addRoundedRect(x, y, w, h, DEFAULT_ROUNDED_WIDTH, DEFAULT_ROUNDED_WIDTH)

    painter.fillPath(path, color)

    painter.setPen(default_line_pen(width=width))
    painter.drawPath(path)

    # painter.drawRoundedRect(x, y, w, h, DEFAULT_ROUNDED_WIDTH, DEFAULT_ROUNDED_WIDTH)
    # painter.fillRect(x,y,w,h,QtGui.Qt.white)


def draw_text_at(painter: QtGui.QPainter, x: int, y: int, w: int, h: int, text: str, font: QtGui.QFont = FONT_MD):
    """
    Draw text at given position and size
    """
    painter.setFont(font)
    painter.drawText(x, y, w, h, 0x0004, text)

def fill_svg(img: QtGui.QPixmap, color: QtGui.QColor):
    qp = QtGui.QPainter(img)
    qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    qp.fillRect(img.rect(), color)
    qp.end()