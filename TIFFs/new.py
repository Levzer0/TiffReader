import sysconfig

import TIFFs.structure
import TIFFs.tools as tools
import binascii
from fractions import Fraction


# TODO test
def new_tiff_from_disk(path, image_file_header, image_file_directories, f):
    """
    new a tiff file, data source from disk
    :param path: path of new tiff
    :param image_file_header: Image File Header of new tiff
    :param image_file_directories: Image File Directories of new tiff
    :param f: file pointer of source file
    """
    with open(path, 'wb+') as r:
        # write Image File Header
        mode = image_file_header['ByteOrder']
        r.write(mode)
        tools.byte_write(r, mode, binascii.unhexlify(image_file_header['FileType']))
        IFD_offset = image_file_header['Offset']
        tools.byte_write(r, mode, IFD_offset.to_bytes(4, byteorder='big', signed=False))
        # write Image File Directories
        for image_file_directory in image_file_directories:
            r.seek(IFD_offset)
            IFD_offset = _write_Image_File_Directory(r, mode, image_file_directory)
        # write data from disk
        for i in range(0, len(image_file_directories)):
            # params of the Image File Directory
            the_IFD = image_file_directories[i]
            strip_offsets = the_IFD['StripOffsets']
            strip_byte_count = the_IFD['StripByteCounts']
            sample_byte = int(the_IFD['BitsPerSample'] / 8)
            # temp params
            the_strip = 0
            r_value_offset = strip_offsets[the_strip]
            for j in range(0, sum(strip_byte_count)):
                # need to write next strip
                if r_value_offset - strip_offsets[the_strip] >= strip_byte_count[the_strip]:
                    the_strip += 1
                    r.seek(strip_offsets[the_strip])
                    r.write(f.read(sample_byte))
                    r_value_offset = r.tell()
                # write in the same strip
                else:
                    r.write(f.read(sample_byte))
                    r_value_offset = r.tell()


def new_tiff_from_memory(path, image_file_header, image_file_directories, data):
    """
    new a tiff file, data source from array
    :param path: path of new tiff
    :param image_file_header: Image File Header of new tiff
    :param image_file_directories: Image File Directories of new tiff
    :param data: source data list, include each band data
    """
    with open(path, 'wb+') as r:
        # write Image File Header
        mode = image_file_header['ByteOrder']
        r.write(mode)
        tools.byte_write(r, mode, binascii.unhexlify(image_file_header['FileType']))
        IFD_offset = image_file_header['Offset']
        tools.byte_write(r, mode, IFD_offset.to_bytes(4, byteorder='big', signed=False))
        # write Image File Directories
        for image_file_directory in image_file_directories:
            r.seek(IFD_offset)
            IFD_offset = _write_Image_File_Directory(r, mode, image_file_directory)
        # write data from memory
        for i in range(0, len(data)):
            # params of the Image File Directory
            the_IFD = image_file_directories[i]
            strip_offsets = the_IFD['StripOffsets']
            strip_byte_count = the_IFD['StripByteCounts']
            sample_byte = int(the_IFD['BitsPerSample'] / 8)
            sample_format = the_IFD['SampleFormat']
            # temp params
            the_strip = 0
            value_offset = strip_offsets[the_strip]
            # TODO add verify of input data length for security
            # calculate every value offset and write data
            for j in range(0, len(data[i])):
                used_strip_byte = sum(strip_byte_count[0:the_strip + 1])
                # if need to write in next strip
                if (j + 1) * sample_byte > used_strip_byte:
                    the_strip += 1
                    r.seek(strip_offsets[the_strip])
                    tools.byte_write(r, mode, tools.value_to_bytes_SampleFormat(data[i][j], sample_format, sample_byte))
                    value_offset = r.tell()
                # write in the strip
                else:
                    r.seek(value_offset)
                    tools.byte_write(r, mode, tools.value_to_bytes_SampleFormat(data[i][j], sample_format, sample_byte))
                    value_offset = r.tell()


def _write_Image_File_Directory(f, mode, image_file_directory):
    """
    write one Image File Directory to File
    :param f: file pointer
    :param mode: tiff byteorder sign
    :param image_file_directory: Image File Directory
    :return: value offset of next Image File Directory
    """
    # get byteorder in str
    m = 'big'
    # Directory Entry value offset
    value_offset = 12 * image_file_directory['DirectoryEntriesNumber'] + 6 + f.tell()

    for key in image_file_directory:
        # write Directory Entry
        if image_file_directory[key] is not None:
            if key in TIFFs.structure.DIRECTORY and key in TIFFs.structure.TAG.values():
                value = image_file_directory[key]
                # more than one value
                if type(value) == list:
                    # get tiff type of value list
                    value_number = len(value)
                    value_type = tools.get_tiff_type(value[0])
                    for i in range(0, value_number):
                        the_type = tools.get_tiff_type(value[i])
                        # in tiff standard, signed is bigger than unsigned, 32-bit type is bigger than 8-bit type
                        # so compare the type code and choose the bigger one
                        if the_type > value_type:
                            value_type = the_type
                    # write tag, Type, Count
                    tools.byte_write(f, mode, TIFFs.structure.TAG_CODE[key].to_bytes(2, byteorder=m, signed=False))
                    tools.byte_write(f, mode, value_type.to_bytes(2, byteorder=m, signed=False))
                    tools.byte_write(f, mode, value_number.to_bytes(4, byteorder=m, signed=False))
                    # bytes size > 4, write behind Directory Entry
                    if TIFFs.structure.FIELD[value_type] * value_number > 4:
                        # write offset
                        tools.byte_write(f, mode, value_offset.to_bytes(4, byteorder=m, signed=False))
                        sign = f.tell()
                        # write value
                        f.seek(value_offset)
                        for i in range(0, value_number):
                            value_bytes = tools.value_to_bytes_FieldType(value[i], value_type)
                            tools.byte_write(f, mode, value_bytes)
                        # record new value_offset
                        value_offset = f.tell()
                        f.seek(sign)
                    # bytes size <= 4, write in Directory Entry
                    else:
                        sign = f.tell()
                        # TODO may cause error
                        for i in range(0, value_number):
                            value_bytes = tools.value_to_bytes_FieldType(value[i], value_type)
                            tools.byte_write(f, mode, value_bytes)
                        # if bytes size < 4, jump to next Directory Entry
                        f.seek(sign + 4)
                # single value
                else:
                    value_type = tools.get_tiff_type(value)
                    # write tag, Type, Count
                    tools.byte_write(f, mode, TIFFs.structure.TAG_CODE[key].to_bytes(2, byteorder=m, signed=False))
                    tools.byte_write(f, mode, value_type.to_bytes(2, byteorder=m, signed=False))
                    tools.byte_write(f, mode, b'\x00\x00\x00\x01')
                    # bytes size > 4, write behind Directory Entry
                    if TIFFs.structure.FIELD[value_type] > 4:
                        # write offset
                        tools.byte_write(f, mode, value_offset.to_bytes(4, byteorder=m, signed=False))
                        sign = f.tell()
                        # write value
                        f.seek(value_offset)
                        value_bytes = tools.value_to_bytes_FieldType(value, value_type)
                        tools.byte_write(f, mode, value_bytes)
                        # record new value_offset
                        value_offset = f.tell()
                        f.seek(sign)
                    else:
                        sign = f.tell()
                        value_bytes = tools.value_to_bytes_FieldType(value, value_type)
                        tools.byte_write(f, mode, value_bytes)
                        # if bytes size < 4, jump to next Directory
                        f.seek(sign + 4)
            # attributes not in TAG
            else:
                # write number of Directory Entries
                if key == 'DirectoryEntriesNumber':
                    tools.byte_write(f, mode, image_file_directory[key].to_bytes(2, byteorder=m, signed=False))
                # write offset of next IFD
                if key == 'NextIFDOffset':
                    tools.byte_write(f, mode, image_file_directory[key].to_bytes(4, byteorder=m, signed=False))
                else:
                    print("unexpected tag")
                    continue
    # return end of the Directory Entry
    return value_offset
