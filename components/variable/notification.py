from dataclasses import dataclass, field
import utils.drawing
from utils.colors import Colors
from utils.icons import Icons
from utils.painter.painter import Painter
from components.variable.watchable_variable import WatchableVariable

class NotificationUpdateEvent:
    def __init__(self):
        self.state = True

    def set(self):
        self.state = True

    def isset(self) -> bool:
        return self.state

    def unset(self):
        self.state = False

class NotificationList:
    """Interface of list with notifications"""

    def renew(self) -> None:
        """Renew notification list"""
        raise NotImplementedError()

    def get_all(self) -> dict[str, "Notification"]:
        """Get visible notifications"""
        raise NotImplementedError()

    def set(self, iden: str, value: bool):
        """Set a notification to a value for visibility"""
        raise NotImplementedError()

@dataclass
class StaticNotificationList(NotificationList):
    """State of current notifications, used as reference"""
    notifications: dict[str, "Notification"]
    update_event: "NotificationUpdateEvent"
    __visible_notifications: dict[str, "Notification"] = field(default_factory=dict)

    def renew(self):
        self.update_event.unset()
        self.__visible_notifications = {iden: n for iden,n in self.notifications.items() if n.is_visible()}
    
    def get_all(self):
        if self.update_event.isset():
            self.renew()

        return self.__visible_notifications

    def set(self, iden, value):
        self.notifications[iden].set_visible(value)

@dataclass
class Notification:
    """Notification with a message and a style"""
    message: str
    style: "NotificationStyle"
    update_event: "NotificationUpdateEvent"
    variable: WatchableVariable

    def is_visible(self):
        return self.variable.get_value() == 1

    def set_visible(self, visible: bool):
        self.variable.set_value(1 if visible else 0)
        self.update_event.set()

    def draw(self, painter: Painter, x:int, y:int, w:int, h:int):
        self.style.draw(self.message, painter, x, y, w, h)

class NotificationStyle:
    """Interface for how a notification should be styled"""
    ICON_SIZE = 30
    ICON_MARGIN = 10
    TEXT_HMARGIN = 10
    TEXT_VMARGIN = 17

    def __init__(self, icon:str = Icons.UNKNOWN, color: (int,int,int,int) = (0,0,0,255)):
        self.icon_str = icon
        self.icon_img = None
        self.color = color

    def draw(self, text: str, painter: Painter, x, y, w, h):
        if self.icon_img is None: self.__init_img(painter)

        # painter.setPen(utils.drawing.default_line_pen(self.color))
        self._draw_box(painter, x, y, w, h)
        self._draw_icon(painter, x, y)
        self._draw_text(text, painter, x, y, w, h)

    def _draw_box(self, painter: Painter, x, y, w, h):
        painter.draw_box(x, y, w, h, self.color)

    def _draw_text(self, text, painter: Painter, x, y, w, h):
        painter.draw_text_at( 
            x+NotificationStyle.ICON_SIZE+NotificationStyle.ICON_MARGIN+NotificationStyle.TEXT_HMARGIN, 
            y+NotificationStyle.TEXT_VMARGIN, 
            w-NotificationStyle.ICON_SIZE-NotificationStyle.ICON_MARGIN-NotificationStyle.TEXT_HMARGIN, 
            h,
            self.color,
            text,
            Painter.FONT_SM)
    
    def _draw_icon(self, painter: Painter, x, y):
        painter.draw_svg(self.icon_img, x+NotificationStyle.ICON_MARGIN, y+NotificationStyle.ICON_MARGIN, 
            NotificationStyle.ICON_SIZE, NotificationStyle.ICON_SIZE, self.color)

        # utils.drawing.fill_svg(self.icon_img, self.color)
        # painter.drawPixmap(x+NotificationStyle.ICON_MARGIN, y+NotificationStyle.ICON_MARGIN, 
        #     NotificationStyle.ICON_SIZE, NotificationStyle.ICON_SIZE, self.icon_img)
    
    def __init_img(self, painter: Painter):
        self.icon_img = painter.get_image_from(self.icon_str)

class NotificationStyles:
    ERROR = lambda : NotificationStyle(Icons.WARNING, Colors.RED)
    WARNING = lambda : NotificationStyle(Icons.WARNING, Colors.ORANGE)
    WARNING_BATTERY = lambda : NotificationStyle(Icons.BATTERY, Colors.ORANGE)
    CRUCIAL = lambda : NotificationStyle(Icons.WARNING, Colors.RED)