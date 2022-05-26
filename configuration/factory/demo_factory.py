from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.test_interval import TestOnInterval

class DemoFactory():
    def create(self):
        readable = TestOnInterval()
        supervisor = SimpleComSupervisor(readable)
        config = DemoDashboardConfig(supervisor=supervisor)

        return config