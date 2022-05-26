from configuration.dashboard_config import DashboardConfig

class Setup():
    """
    Interface for app setup
    """

    def create(self) -> DashboardConfig:
        """
        Sets up app configuration.
        Returns a DashboardConfig object.
        """
        raise NotImplementedError()