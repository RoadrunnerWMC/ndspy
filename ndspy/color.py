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

# Support for DS color values (A1BGR5), which are canonically represented
# in ndspy as (r, g, b, a) tuples (where r, g and b range from 0 to 31 and
# a is 0 or 1). These are used in palettes, A1BGR5 textures, lighting colors,
# and other places.

# Colors with 5-bit alpha values, as used in ndspy.texture, are not supported
# by this module, since converting those to/from A1BGR5 values is impossible
# without rounding (which you can do manually if you so wish)

import struct

from . import _common


# Avoiding using the already-defined functions here because doing so
# provides a significant speedup, and this code always runs upon startup
# for any program that uses this module (directly or otherwise)
LUT_UNPACKED = [None] * 0x10000
LUT_UNPACKED_255 = [None] * 0x10000
LUT_RGBA_255 = [None] * 0x10000
LUT_ARGB_255 = [None] * 0x10000
LUT_BGRA_255 = [None] * 0x10000
LUT_ABGR_255 = [None] * 0x10000
for i in range(0x10000):
    r = i & 0x1F
    g = (i >> 5) & 0x1F
    b = (i >> 10) & 0x1F
    a = (i >> 15) & 1
    LUT_UNPACKED[i] = (r, g, b, a)

    r255 = r << 3 | r >> 2
    g255 = g << 3 | g >> 2
    b255 = b << 3 | b >> 2
    a255 = 255 if a else 0
    LUT_UNPACKED_255[i] = (r255, g255, b255, a255)

    LUT_RGBA_255[i] = (r255 << 24) | (g255 << 16) | (b255 << 8) | a255
    LUT_ARGB_255[i] = (a255 << 24) | (r255 << 16) | (g255 << 8) | b255
    LUT_BGRA_255[i] = (b255 << 24) | (g255 << 16) | (r255 << 8) | a255
    LUT_ABGR_255[i] = (a255 << 24) | (b255 << 16) | (g255 << 8) | r255


def unpack(color):
    """
    Return the color as a quadruple (r, g, b, a), where a is 0 or 1
    (0 meaning transparent and 1 meaning opaque), and r, g and b are
    between 0 and 31 inclusive.
    """
    return (color & 0x1F,
            (color >> 5) & 0x1F,
            (color >> 10) & 0x1F,
            (color >> 15) & 1)


def pack(r, g, b, a=1):
    """
    Pack these channel values into a color. a should be 0 or 1 (0
    meaning transparent and 1 meaning opaque), and r, g and b should be
    between 0 and 31 inclusive.
    """
    value = r & 0x1F
    value |= (g & 0x1F) << 5
    value |= (b & 0x1F) << 10
    value |= (a & 1) << 15
    return value


def unpack255(color):
    """
    Same as unpack(), but scales each channel to the standard 0-255
    scale. Equivalent to expand(unpack(color)).
    """
    r, g, b, a = unpack(color)
    r = r << 3 | r >> 2
    g = g << 3 | g >> 2
    b = b << 3 | b >> 2
    return (r, g, b, 255 if a else 0)


def pack255(r, g, b, a=255):
    """
    Same as pack(), but expects each channel to be on the standard 0-255
    scale. Equivalent to pack(contract(r, g, b[, a])).
    """
    return pack(((r + 4) << 2) // 33,
                ((g + 4) << 2) // 33,
                ((b + 4) << 2) // 33,
                0 if a < 128 else 1)


def expand(r, g, b, a=1):
    """
    Convert the given channel values, where a is 0 or 1
    (0 meaning transparent and 1 meaning opaque) and r, g and b are
    between 0 and 31 inclusive, into a new (r, g, b, a) tuple, where
    all channels are between 0 and 255.
    """
    r = r << 3 | r >> 2
    g = g << 3 | g >> 2
    b = b << 3 | b >> 2
    return (r, g, b, 255 if a else 0)


def contract(r, g, b, a=255):
    """
    Convert the given channel values, where all are between
    0 and 255, to a new (r, g, b, a) tuple, where a is 0 or 1
    (0 meaning transparent and 1 meaning opaque) and r, g and b are
    between 0 and 31 inclusive.
    """
    return (((r + 4) << 2) // 33,
            ((g + 4) << 2) // 33,
            ((b + 4) << 2) // 33,
            0 if a < 128 else 1)


def load(data):
    """
    Convert two bytes of data representing a color to a matching (r, g, b, a) tuple
    """
    return unpack(data[1] << 8 | data[0])


def save(r, g, b, a=1):
    """
    Convert the given channel values, where a is 0 or 1
    (0 meaning transparent and 1 meaning opaque) and r, g and b are
    between 0 and 31 inclusive, into two bytes.
    """
    v = pack(r, g, b, a)
    return bytes([v & 0xFF, v >> 8])


def loadPalette(data):
    """
    Convert binary data to a list of (r, g, b, a) color tuples, where
    r, g and b are between 0 and 31 inclusive, and a is 0 or 1.
    This is the inverse of savePalette().
    """
    LUT = LUT_UNPACKED
    return [LUT[c] for c in struct.unpack_from(f'<{len(data) // 2}H', data)]


def loadPaletteFromFile(filePath):
    """
    Load a palette from a filesystem file.
    This is the inverse of savePaletteToFile().
    """
    with open(filePath, 'rb') as f:
        return loadPalette(f.read())


def savePalette(colors):
    """
    Convert a list of (r, g, b, a) color tuples to binary data, where
    r, g and b are between 0 and 31 inclusive, and a is 0 or 1.
    This is the inverse of loadPalette().
    """
    return struct.pack(f'<{len(colors)}H', *(pack(*c) for c in colors))


def savePaletteToFile(colors, filePath):
    """
    Convert a list of (r, g, b, a) color tuples to binary data, and save
    it to a filesystem file.
    This is the inverse of loadPaletteFromFile().
    """
    d = savePalette(colors)
    with open(filePath, 'wb') as f:
        f.write(d)
