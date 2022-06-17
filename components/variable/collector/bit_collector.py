from dataclasses import dataclass, field
from components.variable.processor.bit_processor import BitProcessor
from components.variable.collector.collector import Collector

@dataclass
class BitCollector(Collector):
    """
    Collects x bits, adds them to a buffer, 
    and passes it to a processor when buffer is full.
    """
    processor: BitProcessor
    bit_count: int = 0
    bit_count_state: int = 0
    bit_buffer: list[int] = field(default_factory=list)
    result: int = 0

    def __reset(self):
        self.bit_buffer = []
        self.bit_count_state = 0
        self.return_pointer = 0

    def get_value(self) -> int:
        return self.result
    
    def add_to_buffer(self, value) -> int:
        if self.bit_count_state >= self.bit_count:
            self.__reset()

        self.bit_buffer += [value]
        self.bit_count_state += 1
        
        if self.bit_count_state >= self.bit_count:
            self.result = self.processor.process(self.bit_buffer)
            return self.result
        
        return None
