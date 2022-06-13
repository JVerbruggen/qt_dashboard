from utils.com_supervisor.readable.readable import Readable
import serial


class SerialReadable(Readable):
    def __init__(self, device: str, baudrate: int, timeout: int = 1):
        self.s = serial.Serial(device, baudrate, timeout=timeout)

    def read(self):
        return self.s.readline()

    def __enter__(self):
        self.s.__enter__()

    def __exit__(self, *args, **kwargs):
        self.s.__exit__(args, kwargs)
