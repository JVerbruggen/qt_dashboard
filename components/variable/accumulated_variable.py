from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass
from components.variable.collector.byte_collector import Collector

@dataclass
class AccumulatedVariable(WatchableVariable):
    """
    Accumulates set values to one result.
    Uses a processor to process multiple values.
    """
    collector: Collector

    def get_value(self):
        return self.collector.get_value()

    def set_value(self, value: int):
        """ Value is a byte """
        result = self.collector.add_to_buffer(value)
        if result is not None: 
            print("Accumulated", result)
        

