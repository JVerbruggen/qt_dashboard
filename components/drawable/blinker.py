from components.drawable.drawable import Drawable
from PySide6 import QtSvg, QtCore, QtGui
import utils.file

class NoColorSvgBlinker(Drawable):
    def __init__(self, svg_filepath, x:int, y:int, size: int):
        self.svg_filepath = svg_filepath
        self.x = x
        self.y = y
        self.size = size

        svg_bytearray = utils.file.read_file(self.svg_filepath)
        # self.svg = QtSvg.QSvgRenderer(self.svg_filepath)
        self.svg = QtSvg.QSvgRenderer(svg_bytearray)
        # print(self.svg_content)

    def set_color(self, color):
        pass

    def draw(self, painter: QtGui.QPainter):
        self.svg.render(painter, QtCore.QRect(self.x,self.y,self.size,self.size))
        pass

class SvgBlinker(Drawable):
    def __init__(self, svg_filepath, x:int, y:int, size: int):
        self.svg_filepath = svg_filepath
        self.x = x
        self.y = y
        self.size = size

        self.img = QtGui.QPixmap(self.svg_filepath)
        qp = QtGui.QPainter(self.img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        qp.fillRect( self.img.rect(), QtGui.QColor('blue') )
        qp.end()

        self.blink_state = False
        self.interval = 20
        self.interval_state = self.interval
    

    def set_color(self):
        color = QtGui.QColor('blue') if self.blink_state else QtGui.QColor('yellow')
        self.blink_state = not self.blink_state

        qp = QtGui.QPainter(self.img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        qp.fillRect( self.img.rect(), color )
        qp.end()

    def draw(self, painter: QtGui.QPainter):
        self.interval_state -= 1
        if self.interval_state < 0: 
            self.interval_state = self.interval
            self.set_color()

        painter.drawPixmap(self.x-self.size/2,self.y-self.size/2,self.size,self.size,self.img)

        painter.drawPoint(self.x,self.y)

        pass