from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.mock import Mock
from configuration.setup.setup import Setup
from functools import partial

class DemoSetup(Setup):
    """
    Demo app setup.
    Works without serial connection.
    """

    def create(self):
        readable = Mock(interval=0.3, policy={
            "0x18": Mock.random_first_byte,
            "0x687": Mock.all_random_bytes,
            "0x69": partial(Mock.take_from, ["00 00 00 00 00 00 00 00", "01 00 00 00 00 00 00 00"])
        })
        supervisor = SimpleComSupervisor(readable)
        config = DemoDashboardConfig(supervisor=supervisor)

        return config