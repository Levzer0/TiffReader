import binascii
import fractions
import struct
import TIFFs.parse
import TIFFs.tools
import TIFFs.new
from fractions import Fraction

a = TIFFs.parse.Tiff("D:/Temp/vel_0.tif")
IFDs = a.get_ImageFileDirectories()
# IFDs[0]['GeoKeyDirectoryTag'] = [1, 1, 0, 7, 1024, 0, 1, 2, 1025, 0, 1, 2, 2048, 0, 1, 4326, 2049, 34737, 7, 0, 2054, 0, 1, 9102, 2057, 34736, 1, 1, 2059, 34736, 1, 0]
IFH = a.get_ImageFileHeader()
data = a.get_data_matrix()
print(IFDs)
# for i in range(0, len(data[0])):
#     raw = data[0][i]
#     data[0][i] = struct.unpack('!d', binascii.unhexlify(raw))[0]
#
# TIFFs.new.new_tiff_from_memory("D:/Temp/share/vel_1100_point.tif", IFH, IFDs, data)