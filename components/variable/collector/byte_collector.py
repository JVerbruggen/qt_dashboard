from dataclasses import dataclass, field
from components.variable.processor.byte_processor import ByteProcessor
from components.variable.collector.collector import Collector


@dataclass
class ByteCollector(Collector):
    """
    Collects x bytes, adds them to a buffer, 
    and passes it to a processor when buffer is full.
    """
    processor: ByteProcessor
    byte_count: int = 0
    byte_count_state: int = 0
    byte_buffer: list[str] = field(default_factory=list)

    def __reset(self):
        self.byte_buffer = []
        self.byte_count_state = 0

    def add_to_buffer(self, value) -> int:
        self.byte_buffer += [value]
        self.byte_count_state = len(byte_buffer)

        if self.byte_count_state >= self.byte_count:
            result = self.processor.process(self.byte_buffer)
            self.__reset()
            return result

        return None
