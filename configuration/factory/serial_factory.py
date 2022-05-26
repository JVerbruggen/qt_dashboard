from configuration.demo_gauge_config import DemoGaugeConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.serial import SerialReadable

class SerialFactory():
    BAUD = 115200
    SERIAL_DEVICE = "COM3"

    def create(self):
        readable = SerialReadable(self.SERIAL_DEVICE, self.BAUD)
        supervisor = SimpleComSupervisor(readable)
        config = DemoGaugeConfig(supervisor=supervisor)

        return config