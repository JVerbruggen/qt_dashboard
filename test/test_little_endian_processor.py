from components.variable.processor.little_endian_byte_processor import LittleEndianByteProcessor

ENCODING = 'utf-8'

def test_conversion():
    processor = LittleEndianByteProcessor()
    assert processor.process(bytes("01 00", ENCODING)) == 1
    assert processor.process(bytes("0F 00", ENCODING)) == 15
    assert processor.process(bytes("FF 00", ENCODING)) == 255
    assert processor.process(bytes("01 01", ENCODING)) == 257