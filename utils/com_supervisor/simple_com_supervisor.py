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

    def __init__(self, readable: Readable, mappings=None):
        if mappings is None:
            mappings = dict()
        self.mappings = mappings
        self.readable = readable

    def register(self, identifier, variable, mapper):
        l = []
        if identifier in self.mappings: l = self.mappings[identifier]
        l += [(variable, mapper)]
        self.mappings[identifier] = l

    def start(self):
        thread = Thread()
        stop = Event()
        thread._target = partial(self.__loop, stop)
        try:
            thread.start()
        except KeyboardInterrupt:
            sys.exit()
        except SystemExit:
            stop.set()
    
    def get_variable(self, identifier: str):
        if identifier not in self.mappings: return None
        return self.mappings[identifier][0]

    def __update_variable(self, identifier, value):
        if identifier not in self.mappings: return
        mappings = self.mappings[identifier]
        if mappings is None: return
        for (variable, mapper) in mappings:
            mapper.map_to(value, variable)

    def __loop(self, stop_event: Event):
        with self.readable as r:
            while not stop_event.is_set():
                raw_encoded = r.read()
                raw = raw_encoded.decode(self.ENCODING)
                if len(raw) == 0: continue
                data = json.loads(raw) # TODO: Should be unnecessary

                identifier = data["identifier"]
                value = data["value"]

                by = bytes(value, self.ENCODING)

                self.__update_variable(identifier, by)
