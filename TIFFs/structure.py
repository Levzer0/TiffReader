HEADER = ('ByteOrder', 'FileType', 'Offset')

DIRECTORY = ('DirectoryEntriesNumber', 'NewSubfileType', 'SubfileType', 'ImageWidth', 'ImageLength', 'BitsPerSample',
             'Compression',  'PhotometricInterpretation',  'Threshholding',  'CellWidth',  'CellLength',
             'FillOrder',  'DocumentName',  'ImageDescription',  'Make',  'Model',
             'StripOffsets',  'Orientation',  'SamplesPerPixel',  'RowsPerStrip',  'StripByteCounts',
             'MinSampleValue',  'MaxSampleValue',  'XResolution',  'YResolution',  'PlanarConfiguration',
             'PageName',  'XPosition',  'YPosition',  'FreeOffsets', 'FreeByteCounts',
             'GrayResponseUnit',  'GrayResponseCurve',  'T4Options',  'T6Options',  'ResolutionUnit',
             'PageNumber', 'TransferFunction',  'Software',  'DateTime',  'Artist',
             'HostComputer', 'Predictor',  'WhitePoint',  'PrimaryChromaticities',  'ColorMap',
             'HalftoneHints', 'TileWidth',  'TileLength',  'TileOffsets', 'TileByteCounts',
             'InkSet', 'InkNames', 'NumberOflInks', 'DotRange', 'TargetPrinter',
             'ExtraSamples', 'SampleFormat', 'SMinSampleValue', 'SMaxSampleValue', 'TransferRange',
             'JPEGProc', 'JPEGInterchangeFormat', 'JPEGInterchangeFormatLngth', 'JPEGRestartInterval', 'JPEGLosslessPredictors',
             'JPEGPointTransforms', 'JPEGQTables', 'JPEGDCTables', 'JPEGACTables','YCbCrCoefficients',
             'YCbCrSubSampling', 'YCbCrPositioning', 'ReferenceBlackWhite', 'Copyright', 'ModelPixelScaleTag',
             'ModelTiepointTag', 'ModelTransformationTag', 'GeoKeyDirectoryTag', 'GeoDoubleParamsTag', 'GeoAsciiParamsTag',
             'NextIFDOffset')

TAG = {254: 'NewSubfileType', 255: 'SubfileType', 256: 'ImageWidth', 257: 'ImageLength', 258: 'BitsPerSample',
       259: 'Compression', 262: 'PhotometricInterpretation', 263: 'Threshholding', 264: 'CellWidth', 265: 'CellLength',
       266: 'FillOrder', 269: 'DocumentName', 270: 'ImageDescription', 271: 'Make', 272: 'Model',
       273: 'StripOffsets', 274: 'Orientation', 277: 'SamplesPerPixel', 278: 'RowsPerStrip', 279: 'StripByteCounts',
       280: 'MinSampleValue', 281: 'MaxSampleValue', 282: 'XResolution', 283: 'YResolution', 284: 'PlanarConfiguration',
       285: 'PageName', 286: 'XPosition', 287: 'YPosition', 288: 'FreeOffsets', 289: 'FreeByteCounts',
       290: 'GrayResponseUnit', 291: 'GrayResponseCurve', 292: 'T4Options', 293: 'T6Options', 296: 'ResolutionUnit',
       297: 'PageNumber', 301: 'TransferFunction', 305: 'Software', 306: 'DateTime', 315: 'Artist',
       316: 'HostComputer', 317: 'Predictor', 318: 'WhitePoint', 319: 'PrimaryChromaticities', 320: 'ColorMap',
       321: 'HalftoneHints', 322: 'TileWidth', 323: 'TileLength', 324: 'TileOffsets', 325: 'TileByteCounts',
       332: 'InkSet', 333: 'InkNames', 334: 'NumberOflInks', 336: 'DotRange', 337: 'TargetPrinter',
       338: 'ExtraSamples', 339: 'SampleFormat', 340: 'SMinSampleValue', 341: 'SMaxSampleValue', 342: 'TransferRange',
       512: 'JPEGProc', 513: 'JPEGInterchangeFormat', 514: 'JPEGInterchangeFormatLngth', 515: 'JPEGRestartInterval', 517: 'JPEGLosslessPredictors',
       518: 'JPEGPointTransforms', 519: 'JPEGQTables', 520: 'JPEGDCTables', 521: 'JPEGACTables', 529: 'YCbCrCoefficients',
       530: 'YCbCrSubSampling', 531: 'YCbCrPositioning', 532: 'ReferenceBlackWhite', 33432: 'Copyright', 33550: 'ModelPixelScaleTag',
       33922: 'ModelTiepointTag', 34264: 'ModelTransformationTag', 34735: 'GeoKeyDirectoryTag', 34736: 'GeoDoubleParamsTag', 34737: 'GeoAsciiParamsTag'}

TAG_CODE = dict(zip(TAG.values(), TAG.keys()))

FIELD = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8,
         6: 1, 7: 1, 8: 2, 9: 4, 10: 8,
         11: 4, 12: 8}

GEOTIFF_HEADER = ('KeyDirectoryVersion', 'KeyRevision', 'MinorRevision', 'NumberOfKeys')

KEY = {1024: 'GTModelTypeGeoKey', 1025: 'GTRasterTypeGeoKey', 1026: 'GTCitationGeoKey', 2048: 'GeographicTypeGeoKey', 2049: 'GeogCitationGeoKey',
       2050: 'GeogGeodeticDatumGeoKey', 2051: 'GeogPrimeMeridianGeoKey', 2061: 'GeogPrimeMeridianLongGeoKey', 2052: 'GeogLinearUnitsGeoKey', 2053: 'GeogLinearUnitSizeGeoKey',
       2054: 'GeogAngularUnitsGeoKey', 2055: 'GeogAngularUnitSizeGeoKey', 2056: 'GeogEllipsoidGeoKey', 2057: 'GeogSemiMajorAxisGeoKey', 2058: 'GeogSemiMinorAxisGeoKey',
       2059: 'GeogInvFlatteningGeoKey', 2060: 'GeogAzimuthUnitsGeoKey', 2062: 'FuckingGeotiff', 3072: 'ProjectedCSTypeGeoKey', 3073: 'PCSCitationGeoKey', 3074: 'ProjectionGeoKey',
       3075: 'ProjCoordTransGeoKey', 3076: 'ProjLinearUnitsGeoKey', 3077: 'ProjLinearUnitSizeGeoKey', 3078: 'ProjStdParallel1GeoKey', 3079: 'ProjStdParallel2GeoKey',
       3080: 'ProjNatOriginLongGeoKey', 3081: 'ProjNatOriginLatGeoKey', 3082: 'ProjFalseEastingGeoKey', 3083: 'ProjFalseNorthingGeoKey', 3084: 'ProjFalseOriginLongGeoKey',
       3085: 'ProjFalseOriginLatGeoKey', 3086: 'ProjFalseOriginEastingGeoKey', 3087: 'ProjFalseOriginNorthingGeoKey', 3088: 'ProjCenterLongGeoKey', 3089: 'ProjCenterLatGeoKey',
       3090: 'ProjCenterEastingGeoKey', 3091: 'ProjFalseOriginNorthingGeoKey', 3092: 'ProjScaleAtNatOriginGeoKey', 3093: 'ProjScaleAtCenterGeoKey', 3094: 'ProjAzimuthAngleGeoKey',
       3095: 'ProjStraightVertPoleLongGeoKey', 4096: 'VerticalCSTypeGeoKey', 4097: 'VerticalCitationGeoKey', 4098: 'VerticalDatumGeoKey', 4099: 'VerticalUnitsGeoKey'}

GEO_DIRECTORY = ('GTModelTypeGeoKey', 'GTRasterTypeGeoKey', 'GTCitationGeoKey', 'GeographicTypeGeoKey', 'GeogCitationGeoKey',
                 'GeogGeodeticDatumGeoKey', 'GeogPrimeMeridianGeoKey', 'GeogPrimeMeridianLongGeoKey', 'GeogLinearUnitsGeoKey', 'GeogLinearUnitSizeGeoKey',
                 'GeogAngularUnitsGeoKey', 'GeogAngularUnitSizeGeoKey', 'GeogEllipsoidGeoKey', 'GeogSemiMajorAxisGeoKey', 'GeogSemiMinorAxisGeoKey',
                 'GeogInvFlatteningGeoKey', 'GeogAzimuthUnitsGeoKey', 'ProjectedCSTypeGeoKey', 'PCSCitationGeoKey', 'ProjectionGeoKey',
                 'ProjCoordTransGeoKey', 'ProjLinearUnitsGeoKey', 'ProjLinearUnitSizeGeoKey', 'ProjStdParallel1GeoKey', 'ProjStdParallel2GeoKey',
                 'ProjNatOriginLongGeoKey', 'ProjNatOriginLatGeoKey', 'ProjFalseEastingGeoKey', 'ProjFalseNorthingGeoKey', 'ProjFalseOriginLongGeoKey',
                 'ProjFalseOriginLatGeoKey', 'ProjFalseOriginEastingGeoKey', 'ProjFalseOriginNorthingGeoKey', 'ProjCenterLongGeoKey', 'ProjCenterLatGeoKey',
                 'ProjCenterEastingGeoKey', 'ProjFalseOriginNorthingGeoKey', 'ProjScaleAtNatOriginGeoKey', 'ProjScaleAtCenterGeoKey', 'ProjAzimuthAngleGeoKey',
                 'ProjStraightVertPoleLongGeoKey', 'VerticalCSTypeGeoKey', 'VerticalCitationGeoKey', 'VerticalDatumGeoKey', 'VerticalUnitsGeoKey',
                 'FuckingGeotiff')

KEY_ENTRY = ('KeyID', 'TIFFTagLocation', 'Count', 'Value_Offset')