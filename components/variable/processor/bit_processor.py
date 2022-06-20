import struct

class BitProcessor:
    def process(self, value: list[int]):
        """Processes a value using a defined strategy"""
        raise NotImplementedError()

class BigEndianBitProcessor(BitProcessor):
    def process(self, value: list[int]):
        return int("".join(reversed([str(v) for v in value])), 2)

class FloatProcessor(BitProcessor):
    def __init__(self, decimals:int = 8, byteorder: str = "big"):
        self.byteorder = byteorder
        self.strformat = "{:." + str(decimals) + "f}"
    
    def __format(self, f):
        return float(self.strformat.format(f))

    def process(self, value: list[int]):
        vstr = "".join([str(v) for v in value])
        fl = struct.unpack('!f',struct.pack('!I', int(vstr, 2)))[0]
        fl = self.__format(fl)
        return fl