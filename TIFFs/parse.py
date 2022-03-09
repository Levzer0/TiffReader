import binascii
import struct
import TIFFs.structure as tiff_structure
import TIFFs.tools as tools
from fractions import Fraction


class Tiff:
    """
    read metadata from a TIFFs.
    return attributes of the TIFFs.
    """

    image_file_header = dict.fromkeys(tiff_structure.HEADER)

    def __init__(self, path):
        """
        init class with input TIFFs
        :param path: tiff file path
        """
        self.path = path
        self.IFDs = []
        self.geo_directories = []
        # open file and read bytes
        with open(path, 'rb', 0) as tiff:
            # read Image File Header
            self.mode = tiff.read(2)
            file_type = tools.byte_read(tiff, self.mode, 2)
            # judge TIFFs
            if file_type != b'002a':
                print("Invalid Tiff!Please input a real TIFFs!")
                return
            IFD_outset = int(tools.byte_read(tiff, self.mode, 4), 16)
            self.image_file_header['ByteOrder'] = self.mode
            self.image_file_header['FileType'] = file_type
            self.image_file_header['Offset'] = IFD_outset
            # read all Image File Directory
            tiff.seek(IFD_outset, 0)
            the_IFD = self.read_IFD(tiff)
            self.IFDs.append(the_IFD)
            # read other IFD
            next_IFD_offset = the_IFD['NextIFDOffset']
            while next_IFD_offset != 0:
                tiff.seek(next_IFD_offset, 0)
                self.IFDs.append(self.read_IFD(tiff))
                next_IFD_offset = int(tools.byte_read(tiff, self.mode, 2), 16)
            # print(self.IFDs)
            return

    @staticmethod
    def _parse_tiff_type(f, mode, field_type, byte_len):
        """
        read bytes and return value in tiff field type
        :param f: file pointer
        :param mode: tiff byteorder sign
        :param field_type: type of value
        :param byte_len: number of bytes
        :return: the value in python
        """

        raw = tools.byte_read(f, mode, byte_len)
        # transfer by field_type
        # 8-bit unsigned int
        if field_type == 1:
            return int(raw, 16)
        # ASCII
        if field_type == 2:
            return binascii.unhexlify(raw)
        # 16-bit unsigned int
        if field_type == 3:
            return int(raw, 16)
        # 32-bit unsigned int
        if field_type == 4:
            return int(raw, 16)
        # fraction, numerator and denominator are long
        if field_type == 5:
            numerator = int(tools.byte_read(f, mode, 4), 16)
            denominator = int(tools.byte_read(f, mode, 4), 16)
            return Fraction(numerator, denominator)
        # 8-bit signed int
        if field_type == 6:
            return int(raw, 16) - 256
        # undefined, return bytes in hex
        if field_type == 7:
            return raw
        # 16-bit signed int
        if field_type == 8:
            return int(raw, 16) - 65536
        # 32-bit signed int
        if field_type == 9:
            return int(raw, 16) - 4294967296
        # fraction, numerator and denominator are long
        if field_type == 10:
            numerator = int(tools.byte_read(f, mode, 4), 16) - 4294967296
            denominator = int(tools.byte_read(f, mode, 4), 16) - 4294967296
            return Fraction(numerator, denominator)
        # single precision IEEE format
        if field_type == 11:
            return struct.unpack('!f', binascii.unhexlify(raw))[0]
        # double precision IEEE format
        if field_type == 12:
            return struct.unpack('!d', binascii.unhexlify(raw))[0]
        else:
            print("unknown Tiff Image File Directory Entry tag, can't parse")
            return

    @staticmethod
    def _read_geo_directory(image_file_directory):
        """
        parse geotiff key in given Image File Directory
        :return: geo message of the Image File Directory
        """
        # judge geotiff
        if image_file_directory['GeoKeyDirectoryTag'] is None:
            print("the tiff is not geotiff")
            return
        # read geotiff header
        geotiff_header = dict.fromkeys(tiff_structure.GEOTIFF_HEADER)
        geotiff_header['KeyDirectoryVersion'] = image_file_directory['GeoKeyDirectoryTag'][0]
        geotiff_header['KeyRevision'] = image_file_directory['GeoKeyDirectoryTag'][1]
        geotiff_header['MinorRevision'] = image_file_directory['GeoKeyDirectoryTag'][2]
        geotiff_header['NumberOfKeys'] = image_file_directory['GeoKeyDirectoryTag'][3]
        # read geo keys
        geo_directory = dict.fromkeys(tiff_structure.GEO_DIRECTORY)
        for i in range(0, geotiff_header['NumberOfKeys']):
            key_entry = dict.fromkeys(tiff_structure.KEY_ENTRY)
            key_entry['KeyID'] = image_file_directory['GeoKeyDirectoryTag'][4 * i + 4]
            key_entry['TIFFTagLocation'] = image_file_directory['GeoKeyDirectoryTag'][4 * i + 5]
            key_entry['Count'] = image_file_directory['GeoKeyDirectoryTag'][4 * i + 6]
            key_entry['Value_Offset'] = image_file_directory['GeoKeyDirectoryTag'][4 * i + 7]
            if key_entry['TIFFTagLocation'] == 0:
                geo_directory[tiff_structure.KEY[key_entry['KeyID']]] = key_entry['Value_Offset']
            else:
                data = []
                for j in range(0, key_entry['Count']):
                    data.append(image_file_directory[tiff_structure.TAG[key_entry['TIFFTagLocation']]][
                                    key_entry['Value_Offset'] + j])
                geo_directory[tiff_structure.KEY[key_entry['KeyID']]] = data

        return geo_directory

    def read_IFD(self, f):
        """
        read one Image File Directory in the given position in file
        :param f: file pointer
        :return: a dict contain Image File Directory
        """
        mode = self.image_file_header['ByteOrder']
        image_file_directory = dict.fromkeys(tiff_structure.DIRECTORY)
        # read number of Directory Entry
        directory_entry_count = int(tools.byte_read(f, mode, 2), 16)
        image_file_directory['DirectoryEntriesNumber'] = directory_entry_count
        # read Directory Entry
        for i in range(0, directory_entry_count):
            # read tag, field type and number of values
            tag = int(tools.byte_read(f, mode, 2), 16)
            field_type = int(tools.byte_read(f, mode, 2), 16)
            value_number = int(tools.byte_read(f, mode, 4), 16)
            # situation1: last 4 bytes is the value offset
            if value_number * tiff_structure.FIELD[field_type] > 4:
                # read offset and record the position in file
                offset = int(tools.byte_read(f, mode, 4), 16)
                sign = f.tell()
                # read values
                f.seek(offset, 0)
                values = []
                for j in range(0, value_number):
                    values.append(self._parse_tiff_type(f, mode, field_type, tiff_structure.FIELD[field_type]))
                # save values and reposition file reader
                image_file_directory[tiff_structure.TAG[tag]] = values
                f.seek(sign, 0)
            #  situation2: last 4 bytes is the value
            else:
                # more than one value
                if value_number > 1:
                    sign = f.tell()
                    # read values
                    values = []
                    for j in range(0, value_number):
                        values.append(self._parse_tiff_type(f, mode, field_type, tiff_structure.FIELD[field_type]))
                    # save values and reposition file reader
                    image_file_directory[tiff_structure.TAG[tag]] = values
                    f.seek(sign+4, 0)
                # single value
                else:
                    value = self._parse_tiff_type(f, mode, field_type, 4)
                    image_file_directory[tiff_structure.TAG[tag]] = value
        # read offset of next IFD
        image_file_directory['NextIFDOffset'] = int(tools.byte_read(f, mode, 4), 16)
        return image_file_directory

    def get_ImageFileHeader(self):
        """
        return Image File Header of the tiff
        :return: Image File Header of the tiff
        """
        return self.image_file_header

    def get_file_mode(self):
        """
        return tiff byteorder sign
        :return: tiff byteorder sign
        """
        return self.mode

    def get_path(self):
        """
        return path of the tiff
        :return: path of the tiff
        """
        return self.path

    def get_ImageFileDirectory(self):
        """
        return the first Image File Directory of the tiff
        :return: the first Image File Directory of the tiff
        """
        return self.IFDs[0]

    def get_ImageFileDirectories(self):
        """
        return Image File Directories of the tiff
        :return: Image File Directories of the tiff
        """
        return self.IFDs

    def get_geo_directories(self):
        """
        return geo message of the tiff
        :return: geo message of the tiff
        """
        for IFD in self.IFDs:
            self.geo_directories.append(self._read_geo_directory(IFD))

        return self.geo_directories

    def get_data_matrix(self):
        """
        return data of tiff in memory
        :return: tiff data in memory
        """
        bands = []
        for IFD in self.IFDs:
            # pixel size
            sample_bytes = int(IFD['BitsPerSample'] / 8)
            band = []
            # read all strips of the band
            with open(self.path, 'rb', 0) as f:
                for i in range(0, len(IFD['StripOffsets'])):
                    f.seek(IFD['StripOffsets'][i], 0)
                    for j in range(0, int((IFD['StripByteCounts'][i] / sample_bytes))):
                        band.append(tools.byte_read(f, self.mode, sample_bytes))

            bands.append(band)
        return bands

    def get_offset_by_xy(self, row, column):
        """
        return value offset in given position of raster space
        :param row: row of pixel
        :param column: column of pixel
        :return: offset of the pixel's value in disk
        """

    def lonlat_to_xy(self, lon, lat):
        """
        point of Geographic Coordinate Systems to raster space in the tiff
        :param lon: longitude
        :param lat: latitude
        :return:
        """

    def get_offset_by_lonlat(self, lon, lat):
        """
        return value offset of given position of Geographic Coordinate Systems
        :param lon: longitude
        :param lat: latitude
        :return: offset of the pixel's value in disk
        """