# Copyright 2019 RoadrunnerWMC
#
# This file is part of ndspy.
#
# ndspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ndspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ndspy.  If not, see <https://www.gnu.org/licenses/>.

import enum
import struct

from . import _common


class TextureFormat(enum.IntEnum):
    """
    An enum describing the various texture formats (for 3D models) the
    Nintendo DS supports.
    """
    UNKNOWN_0 = 0
    TRANSLUCENT_A3I5 = 1
    PALETTED_2BPP = 2
    PALETTED_4BPP = 3
    PALETTED_8BPP = 4
    TEXELED_4X4 = 5
    TRANSLUCENT_A5I3 = 6
    DIRECT_16_BIT = 7


    def bitsPerPixel1(self):
        """
        Return the number of bits per pixel that this format requires in
        a texture's first data region.
        This is useful for calculating the expected amount of data some
        texture will have, given its width, height and format.
        """
        return {
            type(self).UNKNOWN_0: 0,
            type(self).TRANSLUCENT_A3I5: 8,
            type(self).PALETTED_2BPP: 2,
            type(self).PALETTED_4BPP: 4,
            type(self).PALETTED_8BPP: 8,
            type(self).TEXELED_4X4: 2,
            type(self).TRANSLUCENT_A5I3: 8,
            type(self).DIRECT_16_BIT: 16,
            }[self]


    def bitsPerPixel2(self):
        """
        Return the number of bits per pixel that this format requires in
        a texture's second data region.
        This is useful for calculating the expected amount of data some
        texture will have, given its width, height and format.
        """
        # Only TEXELED_4X4 uses the second data region, and it's 1bpp
        # there. 
        if self == type(self).TEXELED_4X4:
            return 1
        else:
            return 0


class TextureCoordinatesTransformationMode(enum.IntEnum):
    """
    An enum describing the four ways texture coordinates can be
    transformed.
    See https://problemkaputt.de/gbatek.htm#ds3dtexturecoordinates
    for more.
    """
    NONE = 0
    TEX_COORD = 1
    NORMAL = 2
    VERTEX = 3


class Texture:
    """
    A texture for a 3D model. May depend on a palette.
    """
    def __init__(self, unk00, unk02, params, unk04, data1, data2):
        self.unk00 = unk00
        self.unk02 = unk02

        self.repeatS = bool(params & 1)                 # TODO: figure out what this means
        self.repeatT = bool(params & 2)                 # TODO: figure out what this means
        self.mirrorS = bool(params & 4)                 # TODO: figure out what this means
        self.mirrorT = bool(params & 8)                 # TODO: figure out what this means
        self.width = 8 << ((params >> 4) & 7)
        self.height = 8 << ((params >> 7) & 7)
        self.format = TextureFormat((params >> 10) & 7)
        self.isColor0Transparent = bool(params & 0x2000)
        self.coordsTransformationMode = TextureCoordinatesTransformationMode(
            (params >> 14) & 3)

        self.unk04 = unk04
        self.data1 = data1
        self.data2 = data2


    @classmethod
    def fromFlags(cls, unk00, unk02, repeatS, repeatT, mirrorS, mirrorT,
            width, height, format, isColor0Transparent,
            coordsTransformationMode, unk04, data1, data2):
        self = cls(unk00, unk02, 0, unk04, data1, data2)
        self.repeatS = repeatS
        self.repeatT = repeatT
        self.mirrorS = mirrorS
        self.mirrorT = mirrorT
        self.width = width
        self.height = height
        self.format = format
        self.isColor0Transparent = isColor0Transparent
        self.coordsTransformationMode = coordsTransformationMode
        return self


    def save(self):
        params = 0

        if self.repeatS: params |= 1
        if self.repeatT: params |= 2
        if self.mirrorS: params |= 4
        if self.mirrorT: params |= 8

        SIZES_ENCODED = {
            8:    0,
            16:   1,
            32:   2,
            64:   3,
            128:  4,
            256:  5,
            512:  6,
            1024: 7,
        }

        if self.width not in SIZES_ENCODED:
            raise ValueError(f'Texture width (currently {self.width})'
                ' must be a power of 2 between 8 and 1024 inclusive!')
        if self.height not in SIZES_ENCODED:
            raise ValueError(f'Texture height (currently {self.height})'
                ' must be a power of 2 between 8 and 1024 inclusive!')

        params |= SIZES_ENCODED[self.width] << 4
        params |= SIZES_ENCODED[self.height] << 7

        params |= (self.format & 7) << 10
        if self.isColor0Transparent: params |= 0x2000
        params |= (self.coordsTransformationMode & 3) << 14

        return self.unk00, self.unk02, params, self.unk04, self.data1, self.data2


    def __str__(self):
        format = {
            int(TextureFormat.UNKNOWN_0): 'unknown-0',
            int(TextureFormat.TRANSLUCENT_A3I5): 'translucent-a3i5',
            int(TextureFormat.PALETTED_2BPP): 'paletted-2bpp',
            int(TextureFormat.PALETTED_4BPP): 'paletted-4bpp',
            int(TextureFormat.PALETTED_8BPP): 'paletted-8bpp',
            int(TextureFormat.TEXELED_4X4): 'texeled-4x4',
            int(TextureFormat.TRANSLUCENT_A5I3): 'translucent-a5i3',
            int(TextureFormat.DIRECT_16_BIT): 'direct-16-bit',
            }[self.format]
        return f'<texture {format} {self.width}x{self.height}>'


    def __repr__(self):
        try:
            argsList = list(self.save())

            # Params
            argsList[2] = hex(argsList[2])

            # Datas 1 & 2
            argsList[4] = _common.shortBytesRepr(argsList[4])
            argsList[5] = _common.shortBytesRepr(argsList[5])

            args = ', '.join(str(x) for x in argsList)

        except Exception:
            args = '...'

        return f'{type(self).__name__}({args})'


class Palette:
    """
    A palette as used in 3D model textures.
    Contains a colors list as well as some other metadata.
    """
    def __init__(self, unk00, unk02, unkHeader02, data):
        self.unk00 = unk00
        self.unk02 = unk02
        self.unkHeader02 = unkHeader02

        if len(data) % 2 == 1:
            raise ValueError(f'Palette data length is {len(data)} (must be even)')
        self.colors = list(struct.unpack(f'<{len(data) // 2}H', data))


    def save(self):
        data = struct.pack(f'<{len(self.colors)}H', *self.colors)
        return self.unk00, self.unk02, self.unkHeader02, data


    @classmethod
    def fromColors(cls, unk00, unk02, unkHeader02, colors):
        self = cls(unk00, unk02, unkHeader02, b'')
        self.colors = colors
        return self


    def __str__(self):
        return f'<palette ({len(self.colors)} colors) {_common.shortColorsListRepr(self.colors)}>'


    def __repr__(self):
        return (f'{type(self).__name__}.fromColors('
            f'{self.unk00},'
            f' {self.unk02},'
            f' {self.unkHeader02},'
            f' {_common.shortColorsListRepr(self.colors)})')


class NSBTX:
    """
    Similar to NSBMD, but only contains textures and palettes (no 3D
    data).
    """
    def __init__(self, data=None):
        if data is not None:
            self._initFromData(data)


    def _initFromData(self, data):
        """
        Load the NSBTX from file data.
        """
        if not data.startswith(b'BTX0'):
            raise ValueError('Invalid NSBTX: incorrect magic')

        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)
        if version != 1:
            raise ValueError(f'Unsupported NSBTX version: {version}')
        
        assert numblocks == 1

        TEX0 = data[0x14:]
        assert TEX0.startswith(b'TEX0')

        parsed = _readTEX0(TEX0)
        self.unk08 = parsed['unk08']
        self.unk10 = parsed['unk10']
        self.unk18 = parsed['unk18']
        self.unk20 = parsed['unk20']
        self.unk2C = parsed['unk2C']
        self.unk32 = parsed['unk32']
        self.textures = parsed['textures']
        self.palettes = parsed['palettes']


    @classmethod
    def fromTexturesAndPalettes(cls, unk08, unk10, unk18, unk20, unk2C, unk32, textures, palettes):
        self = cls()
        self.unk08 = unk08
        self.unk10 = unk10
        self.unk18 = unk18
        self.unk20 = unk20
        self.unk2C = unk2C
        self.unk32 = unk32
        self.textures = textures
        self.palettes = palettes
        return self


    def save(self):
        """
        Save the NSBTX back to a file.
        """
        texInfo = {}
        texInfo['unk08'] = self.unk08
        texInfo['unk10'] = self.unk10
        texInfo['unk18'] = self.unk18
        texInfo['unk20'] = self.unk20
        texInfo['unk2C'] = self.unk2C
        texInfo['unk32'] = self.unk32
        texInfo['textures'] = self.textures
        texInfo['palettes'] = self.palettes
        TEX0 = _saveTEX0(texInfo)

        data = bytearray(0x14)
        data.extend(TEX0)

        # Add the NDS standard file header
        _common.NDS_STD_FILE_HEADER.pack_into(data, 0,
            b'BTX0', 0xFEFF, 1, len(data), 0x10, 1)

        # Insert the offset to the TEX0 block
        data[0x10] = 0x14

        # And return.
        return bytes(data)


def _readTEX0(data):
    """
    Read a TEX0 block.
    Return a bunch of data as a dict.
    """
    assert data.startswith(b'TEX0')

    returnVal = {}

    # TEX0 header
    (unk08, texDataLen, texOff,
            unk10, texDataOff, unk18, compressedData1Len, compressedInfoOff,
            unk20, compressedData1Off, compressedData2Off, unk2C,
            palDataLen, unk32, palOff, palDataOff) = \
        struct.unpack_from('<IHH3IHH4IHH2I', data, 0x8)
    returnVal['unk08'] = unk08
    returnVal['unk10'] = unk10
    returnVal['unk18'] = unk18
    returnVal['unk20'] = unk20
    returnVal['unk2C'] = unk2C
    returnVal['unk32'] = unk32

    texDataLen <<= 3
    palDataLen <<= 3
    compressedData1Len <<= 3
    compressedData2Len = compressedData1Len // 2

    # Textures
    returnVal['textures'] = []
    for name, unk00, unk02, texHeader in _common.loadInfoBlock(data, texOff, 8):
        thisTexOff, params, unk04 = struct.unpack('<HHI', texHeader)
        thisTexOff <<= 3

        tex = Texture(unk00, unk02, params, unk04, b'', b'')

        if tex.format == TextureFormat.TEXELED_4X4:
            thisTexOff1 = compressedData1Off + texDataOff
            thisTexOff2 = compressedData2Off + texDataOff // 2
            thisTexDataLen1 = int(tex.width * tex.height * tex.format.bitsPerPixel1() / 8)
            thisTexDataLen2 = int(tex.width * tex.height * tex.format.bitsPerPixel2() / 8)
            thisTexData1 = data[thisTexOff1 : thisTexOff1 + thisTexDataLen1]
            thisTexData2 = data[thisTexOff2 : thisTexOff2 + thisTexDataLen2]
        else:
            thisTexOff += texDataOff
            thisTexDataLen = int(tex.width * tex.height * tex.format.bitsPerPixel1() / 8)
            thisTexData1 = data[thisTexOff : thisTexOff+thisTexDataLen]
            thisTexData2 = b''

        tex.data1 = thisTexData1
        tex.data2 = thisTexData2

        returnVal['textures'].append((name, tex))

    # Palettes
    # This needs to be done in 2 passes because palettes don't have a
    # "data length" value: first we collect all the palette data start
    # positions (and metadata), then we sort the data start positions,
    # and then we make the actual Palette objects with the palette data.
    paletteStartOffsets = []
    palette2StartOffset = {}

    paletteTuples = []
    returnVal['palettes'] = []

    for name, unk00, unk02, palHeader in _common.loadInfoBlock(data, palOff, 4):
        thisPalOff, unkHeader02 = struct.unpack('<HH', palHeader)
        thisPalOff <<= 3
        thisPalOff += palDataOff

        pt = (name, unk00, unk02, unkHeader02)

        paletteStartOffsets.append(thisPalOff)
        palette2StartOffset[pt] = thisPalOff
        paletteTuples.append(pt)

    paletteStartOffsets.append(palDataOff + palDataLen)
    paletteStartOffsets.sort()

    for pt in paletteTuples:
        startOff = palette2StartOffset[pt]
        endOff = paletteStartOffsets[paletteStartOffsets.index(startOff) + 1]
        palData = data[startOff : endOff]

        name, unk00, unk02, unkHeader02 = pt
        pal = Palette(unk00, unk02, unkHeader02, palData)
        returnVal['palettes'].append((name, pal))

    return returnVal


def _saveTEX0(fields):
    """
    Given a dict containing TEX0 data (in the format returned by
    _loadTEX0), return a bytes object representing the TEX0 block.
    """

    data = bytearray(0x3C)
    texturesData = bytearray()
    compressedData1 = bytearray()
    compressedData2 = bytearray()
    palettesData = bytearray()

    # Textures header
    compressedInfoOff = len(data)
    texOff = len(data)
    
    entries = []
    for texName, tex in fields['textures']:
        unk00, unk02, params, unk04, data1, data2 = tex.save()

        if tex.format == TextureFormat.TEXELED_4X4:
            thisTexOff = len(compressedData1)
            if len(data1) != len(data2) * 2:
                raise ValueError(f'For texeled 4x4 textures, data1 must'
                    ' be twice as long as data2!'
                    f' (Found lengths: {len(data1)}, {len(data2)})')
            compressedData1.extend(data1)
            compressedData2.extend(data2)
        else:
            thisTexOff = len(texturesData)
            texturesData.extend(data1)

        entryData = struct.pack('<HHI', thisTexOff >> 3, params, unk04)
        entries.append((texName, unk00, unk02, entryData))

    data.extend(_common.saveInfoBlock(entries, 8))

    # Palettes header
    palOff = len(data)
    
    entries = []
    for palName, pal in fields['palettes']:
        unk00, unk02, unkHeader02, thisPaletteData = pal.save()
        if len(thisPaletteData) % 8:
            # 4 colors = 8 bytes
            raise ValueError('Palette must be a multiple of 4 colors long')
        thisPalOff = len(palettesData)
        palettesData.extend(thisPaletteData)

        entryData = struct.pack('<HH', thisPalOff >> 3, unkHeader02)
        entries.append((palName, unk00, unk02, entryData))

    data.extend(_common.saveInfoBlock(entries, 4))

    # Data bytearrays
    texDataOff = len(data)
    data.extend(texturesData)
    compressedData1Off = len(data)
    data.extend(compressedData1)
    compressedData2Off = len(data)
    data.extend(compressedData2)
    palDataOff = len(data)
    data.extend(palettesData)

    # TEX0 header
    struct.pack_into('<4sIIHH3IHH4IHH2I', data, 0,
        b'TEX0', len(data), fields['unk08'], len(texturesData) >> 3, texOff,
        fields['unk10'], texDataOff, fields['unk18'], len(compressedData1) >> 3, compressedInfoOff,
        fields['unk20'], compressedData1Off, compressedData2Off, fields['unk2C'],
        len(palettesData) >> 3, fields['unk32'], palOff, palDataOff)

    return bytes(data)
