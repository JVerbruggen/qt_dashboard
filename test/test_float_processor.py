from components.variable.processor.bit_processor import FloatProcessor
import struct

ENCODING = 'utf-8'

def float_to_bits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]

def str_to_intlist(s: str):
    l = []
    for c in s:
        l += [int(c)]
    return l

def test_processor():
    processor = FloatProcessor()
    assert processor.process(str_to_intlist("10000000000000000000000000000000")) == -0.0
    assert processor.process(str_to_intlist("01000011011111110000000000000000")) == 255
    assert processor.process(str_to_intlist("01000110000111000100000000000000")) == 10000
    assert processor.process(str_to_intlist("01000100101101111010000000000000")) == 1469
    assert processor.process(str_to_intlist("01000011110100100000000000000000")) == 420