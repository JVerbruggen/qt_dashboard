from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.test_interval import TestOnInterval
from configuration.setup.setup import Setup

class DemoSetup(Setup):
    """
    Demo app setup.
    Works without serial connection.
    """

    def create(self):
        readable = TestOnInterval()
        supervisor = SimpleComSupervisor(readable)
        config = DemoDashboardConfig(supervisor=supervisor)

        return config