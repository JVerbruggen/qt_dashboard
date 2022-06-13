from configuration.dashboard_config import DashboardConfig
from utils.context.context import Context


class Setup():
    """
    Interface for app setup
    """

    def create(self, window: (int, int), context: Context) -> DashboardConfig:
        """
        Sets up app configuration.
        Returns a DashboardConfig object.
        """
        raise NotImplementedError()
