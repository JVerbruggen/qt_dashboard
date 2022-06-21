from utils.bytes import *


def test_bytes():
    assert byte_to_bit_string(b'00') == '00000000'
    assert byte_to_bit_string(b'0F') == '00001111'
    assert byte_to_bit_string(b'F0') == '11110000'
    assert byte_to_bit_string(b'FF') == '11111111'
    assert byte_to_bit_string(b'0A') == '00001010'
    assert byte_to_bit_string(b'0B') == '00001011'
    assert byte_to_bit_string(b'0C') == '00001100'


def test_int_to_byte():
    assert int_to_byte_str(1) == "01"
    assert int_to_byte_str(15) == "0F"
    assert int_to_byte_str(16) == "10"
    assert int_to_byte_str(255) == "FF"
