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
    bit_result: list[int] = field(default_factory=list)
    return_pointer = 0

    def __reset(self):
        self.bit_buffer = []
        self.bit_count_state = 0
        self.return_pointer = 0

    def get_value(self) -> int:
        print(self.return_pointer)

        if self.return_pointer >= len(self.bit_result): return 0
        v = self.bit_result[self.return_pointer]
        self.return_pointer = (self.return_pointer + 1) % self.bit_count
        print("new return pointer", self.return_pointer)

        return v
    
    def add_to_buffer(self, value) -> int:
        if self.bit_count_state >= self.bit_count:
            self.__reset()

        self.bit_buffer += [value]
        print(f"Collected bit {self.bit_count_state} of {self.bit_count}")
        self.bit_count_state += 1
        
        if self.bit_count_state >= self.bit_count:
            result = self.processor.process(self.bit_buffer)
            self.bit_result = self.bit_buffer
        
        return None
