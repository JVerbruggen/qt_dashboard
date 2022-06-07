from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass
from components.variable.processor.byte_processor import ByteProcessor
from typing import Any

@dataclass
class ProcessedVariable(WatchableVariable):
    value: Any
    processor: ByteProcessor

    def get_value(self):
        return self.value

    def set_value(self, value: int):
        self.value = self.processor.process(value)
        print("Processed", value, "to", self.value)