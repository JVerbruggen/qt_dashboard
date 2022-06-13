from typing import List

from components.drawable.drawable import Drawable

class DashboardConfig:
    """
    Interface for dashboard configuration.
    """

    def get_drawables(self) -> list[Drawable]:
        """
        Returns all drawables for the given window size.
        """
        
        raise NotImplementedError()
    
    def click_event(self, x, y) -> None:
        """
        Handle click event.
        """
        
        raise NotImplementedError()
