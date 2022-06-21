from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.serial import SerialReadable
from configuration.setup.setup import Setup
from utils.context.context import Context


class SerialSetup(Setup):
    """
    App setup with serial communication.
    """

    BAUD = 115200
    SERIAL_DEVICE = "COM3"

    def create(self, context: Context, window):
        readable = SerialReadable(self.SERIAL_DEVICE, self.BAUD)
        supervisor = SimpleComSupervisor(readable)

        environment={}

        config = DemoDashboardConfig(supervisor=supervisor, context=context, window=window, environment=environment)

        return config
