from components.drawable.drawable import Drawable
from components.variable.watchable_variable import WatchableVariable
from utils.colors import Colors
from utils.painter.painter import Painter

class SvgIndicator(Drawable):
    """
    An indicater depicted by a SVG icon that listens to a variable and displays its value (on or off).
    """
    def __init__(self, svg_filepath: str, watchable_variable: WatchableVariable, x: int, y: int, size: int=10, 
            on_color: (int, int, int, int) = Colors.GREEN):
        self.svg_filepath = svg_filepath
        self.watchable_variable = watchable_variable
        self.on_color = on_color
        self.x = x
        self.y = y
        self.size = size
        self.old_state = -1

        self.img = None
        # utils.drawing.fill_svg(self.img, self.on_color)

        self.blink_state = False

    def set_color(self, new_state: int):
        self.blink_state = not self.blink_state
        # utils.drawing.fill_svg(self.img, self.on_color if new_state else Colors.BLACK)

    def draw(self, painter: Painter):
        if self.img is None: self.__init_img(painter)

        current_state = self.watchable_variable.get_value()

        if current_state != self.old_state:
            self.set_color(current_state)

        painter.draw_svg(self.img, int(self.x - self.size / 2), int(self.y - self.size / 2), self.size, self.size, 
            self.on_color if current_state else Colors.BLACK)

        # painter.drawPixmap(int(self.x - self.size / 2), int(self.y - self.size / 2), self.size, self.size, self.img)
    
    def __init_img(self, painter: Painter):
        """Initializes on the first draw."""
        self.img = painter.get_image_from(self.svg_filepath)


class SvgBlinker(SvgIndicator):
    """
    An indicater depicted by a SVG icon that listens to a variable.
    Blinks if value is 1, goes to off color if 0
    """

    def __init__(self, svg_filepath: str, watchable_variable: WatchableVariable, x: int, y: int, size: int=10, interval: int=30,
            on_color: (int, int, int, int) = Colors.GREEN):
        super().__init__(svg_filepath, watchable_variable, x, y, size, on_color)

        self.interval_state = interval
        self.interval = interval
        self.blink_phase = True
        self.blinking = False

    def update_interval(self):
        self.interval_state -= 1
        if self.interval_state <= 0:
            self.blink_phase = not self.blink_phase
            self.interval_state = self.interval

    def set_color(self, new_state: int):
        if new_state == 1:
            if not self.blinking:
                self.blinking = True
                self.interval_state = self.interval

            self.update_interval()
            
        elif self.blinking: 
            self.blinking = False
            self.blink_phase = False

        blink_state = int(self.blink_phase)
        super().set_color(blink_state)
