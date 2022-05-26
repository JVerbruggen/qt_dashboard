from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.serial import SerialReadable
from configuration.setup.setup import Setup

class SerialSetup(Setup):
    """
    App setup with serial communication.
    """

    BAUD = 115200
    SERIAL_DEVICE = "COM3"

    def create(self):
        readable = SerialReadable(self.SERIAL_DEVICE, self.BAUD)
        supervisor = SimpleComSupervisor(readable)
        config = DemoDashboardConfig(supervisor=supervisor)

        return config