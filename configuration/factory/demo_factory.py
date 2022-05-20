from configuration.demo_gauge_config import DemoGaugeConfig
from utils.comreader.serial_reader import SerialReader

class DemoFactory():
    def create(self):
        serial_reader = SerialReader("COM3")
        config = DemoGaugeConfig(comreader=serial_reader)

        return config