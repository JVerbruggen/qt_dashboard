class Drawable:
    """
    A dashboard element that can be drawn
    """
    
    def draw(self, painter):
        raise NotImplementedError()