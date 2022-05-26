from components.drawable.drawable import Drawable

class DashboardConfig:
    """
    Interface for dashboard configuration.
    """

    def get_drawables(self, window: (int, int)) -> list[Drawable]:
        """
        Returns all drawables for the given window size.
        """
        
        raise NotImplementedError()
