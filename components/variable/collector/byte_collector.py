from dataclasses import dataclass, field


@dataclass(slots=True)
class ByteCollector:
    byte_count: int = 0
    byte_count_state: int = 0
    byte_buffer: list[str] = field(default_factory=list)
    processor: ByteProcessor

    def __reset(self):
        byte_buffer = []
        byte_count_state = 0

    def add_to_buffer(self, value) -> int:
        self.byte_buffer += [value]
        self.byte_count_state = len(byte_buffer)

        if self.byte_count_state == self.byte_count:
            result = processor.process(self.byte_buffer)
            self.__reset()
            return result

        return None
