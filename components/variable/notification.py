from dataclasses import dataclass, field
import utils.drawing
from utils.colors import Colors
from PySide6 import QtGui

@dataclass
class NotificationList:
    """State of current notifications"""
    notifications: list["Notification"] = field(default_factory=list)

@dataclass
class Notification:
    message: str
    style: "NotificationStyle"

    def draw(self, painter: QtGui.QPainter, x:int, y:int, w:int, h:int):
        self.style.draw(self.message, painter, x, y, w, h)

class NotificationStyle:
    ICON_SIZE = 30
    ICON_MARGIN = 10
    TEXT_HMARGIN = 10
    TEXT_VMARGIN = 10

    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        raise NotImplementedError() 

class ErrorNotification(NotificationStyle):
    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        raise NotImplementedError() 

class WarningNotification(NotificationStyle):
    ICON_SRC = "assets/warning.svg"

    def __init__(self):
        self.img = QtGui.QPixmap(WarningNotification.ICON_SRC)
        # utils.drawing.fill_svg(self.img, Colors.ORANGE)


    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        painter.setPen(utils.drawing.default_line_pen(Colors.ORANGE))
        utils.drawing.draw_box(painter, x, y, w, h)
        utils.drawing.fill_svg(self.img, Colors.ORANGE)
        painter.drawPixmap(x+NotificationStyle.ICON_MARGIN, y+NotificationStyle.ICON_MARGIN, 
            NotificationStyle.ICON_SIZE, NotificationStyle.ICON_SIZE, self.img)

        utils.drawing.draw_text_at(painter, 
            x+NotificationStyle.ICON_SIZE+NotificationStyle.ICON_MARGIN+NotificationStyle.TEXT_HMARGIN, 
            y+NotificationStyle.TEXT_VMARGIN, 
            w-NotificationStyle.ICON_SIZE-NotificationStyle.ICON_MARGIN-NotificationStyle.TEXT_HMARGIN, 
            h, 
            text,
            utils.drawing.FONT_SM)


class CrucialNotification(NotificationStyle):
    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        raise NotImplementedError() 

class NotificationStyles:
    ERROR = lambda : ErrorNotification()
    WARNING = lambda : WarningNotification()
    CRUCIAL = lambda : CrucialNotification()