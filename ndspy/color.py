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

from . import _common


# These are populated at the bottom of the file.
LUT_UNPACKED = [None] * 0x10000
LUT_UNPACKED_255 = [None] * 0x10000
LUT_RGBA_255 = [None] * 0x10000
LUT_ARGB_255 = [None] * 0x10000
LUT_BGRA_255 = [None] * 0x10000
LUT_ABGR_255 = [None] * 0x10000


def unpack(color):
    """
    Return the color as a quadruple (r, g, b, a), where a is 0 or 1
    (0 meaning opaque and 1 meaning transparent), and r, g and b are
    between 0 and 31 inclusive.
    """
    return (color & 0x1F,
            (color >> 5) & 0x1F,
            (color >> 10) & 0x1F,
            (color >> 15) & 1)


def pack(r, g, b, a=0):
    """
    Pack these channel values into a color. a should be 0 or 1 (0
    meaning opaque and 1 meaning transparent), and r, g and b should be
    between 0 and 31 inclusive.
    """
    value = 0
    value |= r & 0x1F
    value |= (g & 0x1F) << 5
    value |= (b & 0x1F) << 10
    value |= (a & 1) << 15
    return value


def unpack255(color):
    """
    Same as unpack(), but scales each channel to the standard 0-255
    scale.
    """
    r, g, b, a = unpack(color)
    r = r << 3 | r >> 2
    g = g << 3 | g >> 2
    b = b << 3 | b >> 2
    return (r, g, b, 0 if a else 255)


def pack255(r, g, b, a=255):
    """
    Same as pack(), but expects each channel to be on the standard 0-255
    scale.
    """
    return pack(((r + 4) << 2) // 33,
                ((g + 4) << 2) // 33,
                ((b + 4) << 2) // 33,
                1 if a < 128 else 0)


# Avoiding using the already-defined functions here, because doing so
# provides a significant speedup
for i in range(0x10000):
    r = i & 0x1F
    g = (i >> 5) & 0x1F
    b = (i >> 10) & 0x1F
    a = (i >> 15) & 1
    LUT_UNPACKED[i] = (r, g, b, a)

    r255 = r << 3 | r >> 2
    g255 = g << 3 | g >> 2
    b255 = b << 3 | b >> 2
    a255 = 0 if a else 255
    LUT_UNPACKED_255[i] = (r255, g255, b255, a255)

    LUT_RGBA_255[i] = (r255 << 24) | (g255 << 16) | (b255 << 8) | a255
    LUT_ARGB_255[i] = (a255 << 24) | (r255 << 16) | (g255 << 8) | b255
    LUT_BGRA_255[i] = (b255 << 24) | (g255 << 16) | (r255 << 8) | a255
    LUT_ABGR_255[i] = (a255 << 24) | (b255 << 16) | (g255 << 8) | r255
