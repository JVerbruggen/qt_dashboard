import serial
import json
from threading import Thread
from utils.comreader.com_reader import ComReader

class SerialReader(ComReader):
    BAUD = 115200
    ENCODING = 'utf-8'

    def __init__(self, device: str, mappings: dict = dict()):
        self.device = device
        self.mappings = mappings

    def register(self, identifier, variable):
        self.mappings[identifier] = variable

    def start(self):
        thread = Thread(target=self.__loop)
        thread.start()

    def __update_variable(self, identifier, value):
        if identifier not in self.mappings: return
        variable = self.mappings[identifier]
        if variable is None: return
        variable.set_value(value)

    def __loop(self):
        with serial.Serial(self.device, SerialReader.BAUD, timeout=1) as ser:
            while True:
                raw = ser.readline().decode(SerialReader.ENCODING)
                if len(raw) == 0: continue
                data = json.loads(raw) # TODO: Should be unnecessary
                self.__update_variable(data["identifier"], int(data["value"].split()[0], 16))
