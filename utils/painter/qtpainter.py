from utils.painter.painter import Painter
from PySide6 import QtCore, QtWidgets, QtGui

class HMIQtPainter(Painter):
    """Implementation for working with QT"""

    HINT_FONT_SIZE = 18
    VALUE_FONT_SIZE = 25
    DESC_FONT_SIZE = 18

    def __init__(self, painter: QtGui.QPainter):
        self.painter = painter
        self.fonts = self.__init_fonts()

    def draw_rounded_line(self, from_x: int, from_y: int, to_x: int, to_y: int, color: (int,int,int,int), width: int = None):
        self.painter.setPen(self.__default_line_pen(color=color, width=width))
        self.painter.drawLine(QtCore.QLine(from_x, from_y, to_x, to_y))

    def draw_arc(self, cx: int, cy: int, rad: int, start_deg: int, length_deg: int, color: (int,int,int,int), width: int = None):
        self.painter.setPen(self.__default_line_pen(color=color, width=width))
        self.painter.drawArc(cx - rad, cy - rad, rad * 2, rad * 2, start_deg * 16, length_deg * 16)

    def draw_box(self, x: int, y: int, w: int, h: int, color: (int,int,int,int)):
        self.painter.setPen(self.__default_line_pen(color=color))
        self.painter.drawRoundedRect(x, y, w, h, Painter.DEFAULT_ROUNDED_WIDTH, Painter.DEFAULT_ROUNDED_WIDTH)
    
    def draw_box_filled(self, x: int, y: int, w: int, h: int, color: (int,int,int,int), width: int=Painter.DEFAULT_LINE_WIDTH):
        r,g,b,a = color

        color = QtGui.QColor.fromRgb(r,g,b,a)
        path = QtGui.QPainterPath()
        path.addRoundedRect(x, y, w, h, Painter.DEFAULT_ROUNDED_WIDTH, Painter.DEFAULT_ROUNDED_WIDTH)

        self.painter.fillPath(path, color)

        self.painter.setPen(self.__default_line_pen(width=width))
        self.painter.drawPath(path)

    def draw_text_at(self, x: int, y: int, w: int, h: int, color: (int,int,int,int), text: str, font_str: str="TimesMD"):
        self.painter.setPen(self.__default_line_pen(color=color))
        self.painter.setFont(self.__get_font(font_str))
        self.painter.drawText(x, y, w, h, 0x0004, text)

    def draw_svg(self, img, x: int, y: int, w: int, h: int, color: (int,int,int,int)):
        r,g,b,a = color

        qp = QtGui.QPainter(img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        qp.fillRect(img.rect(), QtGui.QColor.fromRgb(r,g,b,a))
        qp.end()

        self.painter.drawPixmap(x, y, w, h, img)

    def get_image_from(self, img_src: str):
        return QtGui.QPixmap(img_src)
    
    def __default_line_pen(self, color: (int,int,int,int) = (200,200,200,255), width: int=Painter.DEFAULT_LINE_WIDTH):
        r,g,b,a = color
        qcolor = QtGui.QColor.fromRgb(r,g,b,a)
        pen = QtGui.QPen(qcolor)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setColor(qcolor)
        pen.setWidth(width)
        return pen

    def __get_font(self, font_str):
        return self.fonts[font_str]

    def __init_fonts(self):
        display_description_font = QtGui.QFont()
        display_description_font.setPixelSize(self.DESC_FONT_SIZE)
        display_description_font.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, 2)

        display_value_font = QtGui.QFont()
        display_value_font.setPixelSize(self.VALUE_FONT_SIZE)
        display_value_font.setBold(True)

        display_hintvalues_font = QtGui.QFont()
        display_hintvalues_font.setPixelSize(self.HINT_FONT_SIZE)
        display_hintvalues_font.setBold(True)
        display_hintvalues_font.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, 1)

        times_sm_bold = QtGui.QFont("Times", 12)
        times_sm_bold.setBold(True)

        return {
            "TimesMD": QtGui.QFont("Times", 13),
            "TimesSM": QtGui.QFont("Times", 12),
            "TimesSMBold" : times_sm_bold,
            "GaugeLG": display_description_font,
            "GaugeMD": display_value_font,
            "GaugeSM": display_hintvalues_font,
        }
