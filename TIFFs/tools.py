import binascii
import fractions
import struct


def byte_read(f, mode, byte_len):
    """
    read bytes in file and return hex bytes in big-endian byte order
    :param f: file pointer
    :param mode: tiff byteorder sign
    :param byte_len: number of bytes
    :return: hex bytes in big-endian byte order
    """
    if mode == b'MM':
        return binascii.hexlify(f.read(byte_len))
    if mode == b'II':
        return binascii.hexlify(f.read(byte_len)[::-1])


def byte_write(f, mode, data):
    """
    write bytes to file in given order
    :param f: file pointer
    :param mode: tiff byteorder sign
    :param data: bytes to write
    :return: none
    """
    if mode == b'MM':
        f.write(data)
    if mode == b'II':
        f.write(data[::-1])


def byteorder_str(mode):
    """
    transfer tiff byteorder sign to python byteorder sign
    :param mode: tiff byteorder sign in bytes
    :return: python byteorder sign in string
    """
    if type(mode) == bytes:
        if mode == b'MM':
            return 'big'
        if mode == b'II':
            return 'little'
    else:
        return mode


def get_tiff_type(value):
    """
    return tiff type of value
    :param value: input data
    :return: tiff type of value
    """
    # int
    if type(value) == int:
        # 8-bit signed int
        if -128 <= value < 0:
            return 6
        # 16-bit signed int
        if -32768 <= value < -128:
            return 8
        # 32-bit signed int
        if value < -32768:
            return 9
        # 8-bit unsigned int
        if 0 <= value <= int(b'ff', 16):
            return 1
        # 16-bit unsigned int
        if int(b'ff', 16) < value <= int(b'ffff', 16):
            return 3
        # 32-bit unsigned int
        if int(b'ffff', 16) < value <= int(b'ffffffff', 16):
            return 4
    # double
    if type(value) == float:
        return 12
    # fraction
    if type(value) == fractions.Fraction:
        # signed fraction
        if value.numerator < 0 or value.denominator < 0:
            return 10
        # unsigned fraction
        else:
            return 5
    # ASCII
    if type(value) == str:
        return 2
    # undefined
    if type(value) == bytes:
        return 7


def value_to_bytes_FieldType(value, field_type):
    """
    transfer value to hex bytes by TIFF6 field type
    :param value: input data
    :param field_type: tiff type code
    :return: bytes of value in hex
    """
    # 8-bit unsigned int
    if field_type == 1:
        return value.to_bytes(1, byteorder='big', signed=False)
    # ASCII
    if field_type == 2:
        return binascii.hexlify(value)
    # 16-bit unsigned int
    if field_type == 3:
        return value.to_bytes(2, byteorder='big', signed=False)
    # 32-bit unsigned int
    if field_type == 4:
        return value.to_bytes(4, byteorder='big', signed=False)
    # fraction, numerator and denominator are long
    if field_type == 5:
        num_bytes = value.numerator.to_bytes(4, byteorder='big', signed=False)
        den_bytes = value.denominator .to_bytes(4, byteorder='big', signed=False)
        return num_bytes + den_bytes
    # 8-bit signed int
    if field_type == 6:
        return value.to_bytes(1, byteorder='big', signed=True)
    # undefined
    if field_type == 7:
        return value
    # 16-bit signed int
    if field_type == 8:
        return value.to_bytes(2, byteorder='big', signed=True)
    # 32-bit signed int
    if field_type == 9:
        return value.to_bytes(4, byteorder='big', signed=True)
    # fraction, numerator and denominator are signed long
    if field_type == 10:
        num_bytes = value.numerator.to_bytes(4, byteorder='big', signed=True)
        den_bytes = value.denominator .to_bytes(4, byteorder='big', signed=True)
        return num_bytes + den_bytes
    # single precision IEEE format
    if field_type == 11:
        return struct.pack('f', value)[::-1]
    # double precision IEEE format
    if field_type == 12:
        return struct.pack('d', value)[::-1]
    else:
        print("unknown Tiff Image File Directory Entry tag, can't parse")
        return


def value_to_bytes_SampleFormat(value, sample_format, size):
    """
    transfer value to hex bytes by TIFF6 sample format
    :param value: input data
    :param sample_format: sample format code
    :param size: size of data samples
    :return: bytes of value in hex
    """
    # unsigned integer data
    if sample_format == 1:
        return value.to_bytes(size, byteorder='big', signed=False)
    # two's complement signed integer data
    if sample_format == 2:
        return value.to_bytes(size, byteorder='big', signed=True)
    # IEEE floating point data[IEEE]
    if sample_format == 3:
        if size == 4:
            return struct.pack('f', value)[::-1]
        if size == 8:
            return struct.pack('d', value)[::-1]
    # undefined data format
    if sample_format == 4:
        if type(value) == bytes:
            return value
        else:
            print("illegal input")
            return
    else:
        print("unknown sample format")
        return
