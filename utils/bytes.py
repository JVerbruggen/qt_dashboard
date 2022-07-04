def byte_to_bit_array(byte):
    return bin(int(byte, 16))


def byte_to_bit_string(byte):
    return "{:08b}".format(int(byte, 16))


def int_to_byte_str(x):
    return "{:02x}".format(x).upper()
