from components.variable.processor.byte_processor import ByteProcessor


class LittleEndianByteProcessor(ByteProcessor):
    def process(self, value):
        return int("".join(value.decode('utf-8').split()[::-1]), 16)