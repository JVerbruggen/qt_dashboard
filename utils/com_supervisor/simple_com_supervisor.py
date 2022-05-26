import json
from threading import Thread, Event
from utils.com_supervisor.com_supervisor import ComSupervisor
from utils.com_supervisor.mapping.mapper import Mapper
from utils.com_supervisor.readable.readable import Readable
from functools import partial
import sys

class SimpleComSupervisor(ComSupervisor):
    """
    Supervises external communication to the dashboard variables.
    Uses a dict to map identifiers to dashboard variables.
    Takes a readable to read info from.
    """

    ENCODING = 'utf-8'

    def __init__(self, readable: Readable, mappings: dict = dict()):
        self.mappings = mappings
        self.readable = readable

    def register(self, identifier, variable, mapper: Mapper):
        self.mappings[identifier] = (variable, mapper)

    def start(self):
        thread = Thread()
        stop = Event()
        thread._target = partial(self.__loop, stop)
        try:
            thread.start()
        except (KeyboardInterrupt):
            stop.set()
            sys.exit()

    def __update_variable(self, identifier, value):
        if identifier not in self.mappings: return
        (variable, mapper) = self.mappings[identifier]
        if variable is None: return
        mapped_value = mapper.map(value)
        variable.set_value(mapped_value)

    def __loop(self, stop_event: Event):
        with self.readable as r:
            while not stop_event.is_set():
                raw = r.read().decode(self.ENCODING)
                if len(raw) == 0: continue
                data = json.loads(raw) # TODO: Should be unnecessary
                self.__update_variable(data["identifier"], data["value"])


