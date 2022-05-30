from dataclasses import dataclass, field
import utils.drawing
from utils.colors import Colors
from utils.icons import Icons
from PySide6 import QtGui

@dataclass
class NotificationList:
    """State of current notifications, used as reference"""
    notifications: list["Notification"] = field(default_factory=list)

@dataclass
class Notification:
    """Notification with a message and a style"""
    message: str
    style: "NotificationStyle"

    def draw(self, painter: QtGui.QPainter, x:int, y:int, w:int, h:int):
        self.style.draw(self.message, painter, x, y, w, h)

class NotificationStyle:
    """Interface for how a notification should be styled"""
    ICON_SIZE = 30
    ICON_MARGIN = 10
    TEXT_HMARGIN = 10
    TEXT_VMARGIN = 10

    def __init__(self, icon:str = Icons.UNKNOWN, color:QtGui.QColor = Colors.BLACK):
        self.icon_img = QtGui.QPixmap(icon)
        self.color = color

    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        raise NotImplementedError() 

    def _draw_text(self, text, painter: QtGui.QPainter, x, y, w, h):
        utils.drawing.draw_text_at(painter, 
            x+NotificationStyle.ICON_SIZE+NotificationStyle.ICON_MARGIN+NotificationStyle.TEXT_HMARGIN, 
            y+NotificationStyle.TEXT_VMARGIN, 
            w-NotificationStyle.ICON_SIZE-NotificationStyle.ICON_MARGIN-NotificationStyle.TEXT_HMARGIN, 
            h, 
            text,
            utils.drawing.FONT_SM)
    
    def _draw_icon(self, painter, x, y):
        utils.drawing.fill_svg(self.icon_img, self.color)
        painter.drawPixmap(x+NotificationStyle.ICON_MARGIN, y+NotificationStyle.ICON_MARGIN, 
            NotificationStyle.ICON_SIZE, NotificationStyle.ICON_SIZE, self.icon_img)

class ErrorNotification(NotificationStyle):
    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        raise NotImplementedError() 

class WarningNotification(NotificationStyle):
    def __init__(self, icon=Icons.WARNING):
        super().__init__(icon, Colors.ORANGE)

    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        painter.setPen(utils.drawing.default_line_pen(self.color))
        utils.drawing.draw_box(painter, x, y, w, h)

        super()._draw_icon(painter, x, y)
        super()._draw_text(text, painter, x, y, w, h)


class CrucialNotification(NotificationStyle):
    def draw(self, text: str, painter: QtGui.QPainter, x, y, w, h):
        raise NotImplementedError() 

class NotificationStyles:
    ERROR = lambda : ErrorNotification()
    WARNING = lambda : WarningNotification()
    WARNING_BATTERY = lambda : WarningNotification(Icons.BATTERY)
    CRUCIAL = lambda : CrucialNotification()