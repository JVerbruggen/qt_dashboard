from dataclasses import dataclass, field
import utils.drawing
from utils.colors import Colors
from utils.icons import Icons
from utils.painter.painter import Painter
from components.variable.watchable_variable import WatchableVariable

class NotificationUpdateEvent:
    """
    Used for redrawing all visible notifications (for optimization).
    Is usually set whenever a variable updates, so that the list knows the visible notifications
    should be recalculated.
    """
    def __init__(self):
        self.state = True

    def set(self):
        self.state = True

    def isset(self) -> bool:
        return self.state

    def unset(self):
        self.state = False

class NotificationList:
    """
    Interface of list with notifications.
    """

    def renew(self) -> None:
        """Renew notification list"""
        raise NotImplementedError()

    def get_all(self) -> dict[str, "Notification"]:
        """Get visible notifications"""
        raise NotImplementedError()

@dataclass
class StaticNotificationList(NotificationList):
    """
    State of current notifications, used as reference.
    """
    notifications: dict[str, "Notification"]
    update_event: "NotificationUpdateEvent"
    from_priority_level: int = 1
    __visible_notifications: dict[str, "Notification"] = field(default_factory=dict)

    def renew(self):
        self.update_event.unset()
        self.__visible_notifications = {iden: n for iden,n in self.notifications.items() if n.is_visible(self.from_priority_level)}
    
    def get_all(self):
        if self.update_event.isset():
            self.renew()

        return self.__visible_notifications

@dataclass
class Notification:
    """Notification with a message and a style"""
    def is_visible(self, from_priority_level: int):
        raise NotImplementedError()

    def draw(self, painter: Painter, x:int, y:int, w:int, h:int):
        raise NotImplementedError()

@dataclass
class SimpleNotification(Notification):
    """
    Simple notification that can be visible or not.
    """
    title: str
    message: str
    style: "NotificationStyle"
    update_event: "NotificationUpdateEvent"
    variable: WatchableVariable
    priority: int = 1
    __last_state: int = -1

    def is_visible(self, from_priority_level):
        return self.priority >= from_priority_level \
            and self.variable.get_value() == 1

    def draw(self, painter: Painter, x:int, y:int, w:int, h:int):
        value = self.variable.get_value()
        if value != self.__last_state:
            self.__last_state = value
            self.update_event.set()

        self.style.draw(self.title, self.message, painter, x, y, w, h)

@dataclass
class MultipleNotification(Notification):
    """
    Notification that is always displayed. Displayed text is determined by variable.
    I.e. if variable == 0, displayed message will be messages[0].
    """
    title: str
    messages: list[str]
    style: "NotificationStyle"
    update_event: "NotificationUpdateEvent"
    variable: WatchableVariable
    priority: int = 1
    __last_state: int = -1

    def is_visible(self, from_priority_level):
        return self.priority >= from_priority_level

    def draw(self, painter: Painter, x:int, y:int, w:int, h:int):
        value = self.variable.get_value()
        if value != self.__last_state:
            self.__last_state = value
            self.update_event.set()

        self.style.draw(self.title, self.messages[value], painter, x, y, w, h)

class NotificationStyle:
    """
    Interface for how a notification should be styled.
    """
    ICON_SIZE = 30
    ICON_MARGIN = 10
    TEXT_HMARGIN = 10
    TEXT_VMARGIN = 17
    TEXT_VOFFSET = 8

    def __init__(self, icon:str = Icons.UNKNOWN, color: (int,int,int,int) = (0,0,0,255)):
        self.icon_str = icon
        self.icon_img = None
        self.color = color

    def draw(self, title: str, text: str, painter: Painter, x, y, w, h):
        if self.icon_img is None: self.__init_img(painter)

        self._draw_box(painter, x, y, w, h)
        self._draw_icon(painter, x, y)
        self._draw_text(title, painter, x, y-self.TEXT_VOFFSET, w, h, font=Painter.FONT_SM_BOLD)
        self._draw_text(text, painter, x, y+self.TEXT_VOFFSET, w, h)

    def _draw_box(self, painter: Painter, x, y, w, h):
        painter.draw_box(x, y, w, h, self.color)

    def _draw_text(self, text, painter: Painter, x, y, w, h, font=Painter.FONT_SM):
        painter.draw_text_at( 
            x+NotificationStyle.ICON_SIZE+NotificationStyle.ICON_MARGIN+NotificationStyle.TEXT_HMARGIN, 
            y+NotificationStyle.TEXT_VMARGIN, 
            w-NotificationStyle.ICON_SIZE-NotificationStyle.ICON_MARGIN-NotificationStyle.TEXT_HMARGIN, 
            h,
            self.color,
            text,
            font)
    
    def _draw_icon(self, painter: Painter, x, y):
        painter.draw_svg(self.icon_img, x+NotificationStyle.ICON_MARGIN, y+NotificationStyle.ICON_MARGIN, 
            NotificationStyle.ICON_SIZE, NotificationStyle.ICON_SIZE, self.color)
    
    def __init_img(self, painter: Painter):
        self.icon_img = painter.get_image_from(self.icon_str)

class NotificationStyles:
    """
    Preset NotificationStyle objects.
    """
    ERROR = lambda : NotificationStyle(Icons.WARNING, Colors.RED)
    WARNING = lambda : NotificationStyle(Icons.WARNING, Colors.ORANGE)
    WARNING_BATTERY = lambda : NotificationStyle(Icons.BATTERY, Colors.ORANGE)
    CRUCIAL = lambda : NotificationStyle(Icons.WARNING, Colors.RED)
    INFO = lambda : NotificationStyle(Icons.UNKNOWN, Colors.GREEN)

    def from_iden(iden: str):
        if iden == "info": return NotificationStyles.INFO()
        elif iden == "warning": return NotificationStyles.WARNING()
        elif iden == "warning-battery": return NotificationStyles.WARNING_BATTERY()
        elif iden == "error": return NotificationStyles.ERROR()
        elif iden == "crucial": return NotificationStyles.CRUCIAL()