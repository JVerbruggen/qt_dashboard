from components.drawable.drawable import Drawable
from components.variable.notification import NotificationList
from dataclasses import dataclass
import utils.drawing
import math

@dataclass
class NotificationBox(Drawable):
    """
    A box of notifications ;)
    """
    notification_list: NotificationList
    x: int
    y: int
    w: int
    h: int
    notification_height: int

    def __draw_notifications(self, painter):
        display_count = math.floor(self.h/self.notification_height)

        for i in range(min(display_count, len(self.notification_list.notifications))):
            nx = self.x
            ny = self.y + i*notification_height
            nw = self.w
            nh = self.notification_height

            n = self.notification_list.notifications[i]
            n.draw(painter, nx, ny, nw, nh)

    def draw(self, painter):
        self.__draw_notifications(painter)

        utils.drawing.draw_box(painter, self.x, self.y, self.w, self.h)

        
        
