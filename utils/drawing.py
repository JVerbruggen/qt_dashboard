from PySide6 import QtCore, QtWidgets, QtGui

def draw_rounded_line(painter: QtGui.QPainter, fromPoint: QtCore.QPoint, toPoint: QtCore.QPoint, width:int=None):
    if width:
        pen = QtGui.QPen(QtGui.Qt.white)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setWidth(width)
        painter.setPen(pen)

    painter.drawLine(QtCore.QLine(fromPoint, toPoint))

def draw_arc(painter: QtGui.QPainter, cx: int, cy: int, rad: int, startDeg: int, lengthDeg: int, width:int=None):
    if width:
        pen = QtGui.QPen(QtGui.Qt.white)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setColor(QtGui.qRgb(200, 200, 200))
        pen.setWidth(width)
        painter.setPen(pen)

    painter.drawArc(cx-rad, cy-rad, rad*2, rad*2, startDeg*16, lengthDeg*16)

def draw_text_at(painter: QtGui.QPainter, x:int, y:int, w:int, h:int, text:str, font:QtGui.QFont=None):
    if font: painter.setFont(font)
    painter.drawText(x,y,w,h,0x0004,text)