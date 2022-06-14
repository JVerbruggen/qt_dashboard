class BitProcessor:
    def process(self, value: list[int]):
        """Processes a value using a defined strategy"""
        raise NotImplementedError()

class BigEndianBitProcessor(BitProcessor):
    def process(self, value: list[int]):
        return int("".join(reversed([str(v) for v in value])), 2)