from dataclasses import dataclass, field

@dataclass
class NotificationList:
    """State of current notifications"""
    notifications: list["Notification"] = field(default_factory=list)

@dataclass
class Notification:
    message: str
    style: "NotificationStyle"

    def draw(self, painter, x:int, y:int, w:int, h:int):
        style.draw(painter, x, y, w, h)

class NotificationStyle:
    def draw(self, painter, x, y, w, h):
        raise NotImplementedError()

class WarningNotification(NotificationStyle):
    def draw(self, painter, x, y, w, h):
        painter.setPen()