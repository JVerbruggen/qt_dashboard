from components.drawable.drawable import Drawable
from components.variable.notification import NotificationList
from dataclasses import dataclass
import utils.drawing
from utils.painter.painter import Painter
import math

@dataclass
class NotificationBox(Drawable):
    """
    A box of notifications
    """
    PADDING = 10

    notification_list: NotificationList
    x: int
    y: int
    w: int
    h: int
    notification_height: int

    def __draw_notifications(self, painter: Painter):
        display_count = math.floor(self.h/(self.notification_height+NotificationBox.PADDING))

        notifications = self.notification_list.get_all().items()

        for i,(iden,n) in zip(range(display_count), notifications):
            nx = self.x
            ny = self.y + i*self.notification_height + i*NotificationBox.PADDING
            nw = self.w
            nh = self.notification_height

            n.draw(painter, nx, ny, nw, nh)

    def draw(self, painter: Painter):
        self.__draw_notifications(painter)
