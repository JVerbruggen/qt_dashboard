from configuration.demo_gauge_config import DemoGaugeConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.test_interval import TestOnInterval

class DemoFactory():
    def create(self):
        readable = TestOnInterval()
        supervisor = SimpleComSupervisor(readable)
        config = DemoGaugeConfig(supervisor=supervisor)

        return config