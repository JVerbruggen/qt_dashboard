from utils.painter.painter import Painter


class Drawable:
    """
    A dashboard element that can be drawn
    """

    def draw(self, painter: Painter):
        raise NotImplementedError()
