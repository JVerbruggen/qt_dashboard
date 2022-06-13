import json
from threading import Thread, Event
from utils.com_supervisor.com_supervisor import ComSupervisor
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

    def register(self, identifier, variable, mapper):
        self.mappings[identifier] = (variable, mapper)

    def start(self):
        thread = Thread()
        stop = Event()
        thread._target = partial(self.__loop, stop)
        try:
            thread.start()
        except (KeyboardInterrupt):
            sys.exit()
        except (SystemExit):
            stop.set()

    def __update_variable(self, identifier, value):
        if identifier not in self.mappings: return
        (variable, mapper) = self.mappings[identifier]
        if variable is None: return
        mapper.map_to(value, variable)

    def __loop(self, stop_event: Event):
        with self.readable as r:
            while not stop_event.is_set():
                raw_encoded = r.read()
                raw = raw_encoded.decode(self.ENCODING)
                if len(raw) == 0: continue
                data = json.loads(raw)  # TODO: Should be unnecessary

                identifier = data["identifier"]
                value = data["value"]

                by = bytes(value, self.ENCODING)

                self.__update_variable(identifier, by)
