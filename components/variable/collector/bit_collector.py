from dataclasses import dataclass, field
from components.variable.processor.bit_processor import BitProcessor
from components.variable.collector.collector import Collector

@dataclass
class BitCollector(Collector):
    processor: BitProcessor
    bit_count: int = 0
    bit_count_state: int = 0
    bit_buffer: list[int] = field(default_factory=list)

    def __reset(self):
        self.bit_buffer = []
        self.bit_count_state = 0
    
    def add_to_buffer(self, value) -> int:
        self.bit_buffer += [value]
        self.bit_count_state += 1
        
        if self.bit_count_state >= self.bit_count:
            result = self.processor.process(self.bit_buffer)
            self.__reset()
            return result
        
        return None
