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
"""
Support for LZ10 compression.
"""


import struct

from . import _lzCommon


def decompress(data):
    """
    Decompress LZ10-compressed data.
    """

    # NOTE:
    # This code is ported from NSMBe, which was converted from Elitemap.

    if data[0] != 0x10:
        raise TypeError("This isn't a LZ10-compressed file.")

    dataLen = struct.unpack_from('<I', data)[0] >> 8

    out = bytearray(dataLen)
    inPos, outPos = 4, 0

    while dataLen > 0:
        d = data[inPos]; inPos += 1

        if d:
            for i in range(8):
                if d & 0x80:
                    thing, = struct.unpack_from('>H', data, inPos); inPos += 2

                    length = (thing >> 12) + 3
                    offset = thing & 0xFFF
                    windowOffset = outPos - offset - 1

                    for j in range(length):
                        out[outPos] = out[windowOffset]
                        outPos += 1; windowOffset += 1; dataLen -= 1

                        if dataLen == 0:
                            return bytes(out)

                else:
                    out[outPos] = data[inPos]
                    outPos += 1; inPos += 1; dataLen -= 1

                    if dataLen == 0:
                        return bytes(out)

                d <<= 1
        else:
            for i in range(8):
                out[outPos] = data[inPos]
                outPos += 1; inPos += 1; dataLen -= 1

                if dataLen == 0:
                    return bytes(out)

    return bytes(out)


def decompressFromFile(filePath):
    """
    Load a LZ10-compressed filesystem file, and decompress it.
    """
    with open(filePath, 'rb') as f:
        return decompress(f.read())


def compress(data):
    """
    Compress data in LZ10 format.
    """

    # NOTE:
    # This code is ported from NSMBe.

    compressed, _, _ = _lzCommon.compress(data, 1, 0x1000, 18, True, False)
    compressed = bytearray(compressed)
    compressed[:0] = struct.pack('<I', (len(data) << 8) | 0x10)
    return bytes(compressed)


def compressToFile(data, filePath):
    """
    Compress data in LZ10 format, and save it to a filesystem file.
    """
    d = compress(data)
    with open(filePath, 'wb') as f:
        f.write(d)
