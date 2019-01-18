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
Support for NARC archives.
"""


import collections
import struct

from . import _common
from . import fnt


def load(data):
    """
    Read NARC data, and create a filename table and a list of files.
    """
    # Read the standard header
    magic, bom, version, filesize, headersize, numblocks = \
        _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)
    if version not in [1, 0x100]:
        raise ValueError(f'Unsupported NARC version: {version}')

    if magic != b'NARC':
        raise ValueError("Wrong magic (should be b'NARC', instead found "
                         f'{magic})')

    # Read the file allocation block
    fatbMagic, fatbSize, fileCount = struct.unpack_from('<4sII', data, 0x10)
    assert fatbMagic == b'FATB'[::-1]

    # Read the file name block
    fntbOffset = 0x10 + fatbSize
    fntbMagic, fntbSize = struct.unpack_from('<4sI', data, fntbOffset)
    assert fntbMagic == b'FNTB'[::-1]

    # Get the data from the file data block before continuing
    fimgOffset = fntbOffset + fntbSize
    fimgMagic, gmifSize = struct.unpack_from('<4sI', data, fimgOffset)
    assert fimgMagic == b'FIMG'[::-1]
    rawDataOffset = fimgOffset + 8

    # Read the file datas
    fileList = []
    for i in range(fileCount):
        startOffset, endOffset = struct.unpack_from('<II', data, 0x1C + 8 * i)
        fileList.append(data[rawDataOffset+startOffset : rawDataOffset+endOffset])

    # Parse the filenames
    names = fnt.load(data[fntbOffset + 8 : fntbOffset + fntbSize])

    return names, fileList


def loadFromFile(filePath):
    """
    Load a NARC archive from a filesystem file, and create a filename
    table and a list of files.
    """
    with open(filePath, 'rb') as f:
        return load(f.read())


def save(filenames, fileList):
    """
    Create a NARC archive from a filename table and a list of files.
    """

    # Prepare the filedata and file allocation table block
    fimgData = bytearray(8)

    fatbData = bytearray()
    fatbData.extend(struct.pack('<4sII',
        b'FATB'[::-1], 0x0C + 8 * len(fileList), len(fileList)))

    # Write data into the FIMG and FAT blocks
    for i, fd in enumerate(fileList):
        startOff = len(fimgData) - 8
        fimgData.extend(fd)
        endOff = startOff + len(fd)
        fatbData.extend(struct.pack('<II', startOff, endOff))
        while len(fimgData) % 4:
            fimgData.append(0)

    # Put the header on the FIMG block
    struct.pack_into('<4sI', fimgData, 0, b'FIMG'[::-1], len(fimgData))

    # Assemble the filename table block
    nameTable = bytearray(fnt.save(filenames))
    while len(nameTable) % 4:
        nameTable.append(0xFF)
    fntbData = struct.pack('<4sI', b'FNTB'[::-1], len(nameTable) + 8) + nameTable

    # Put everything together and return.
    data = bytearray(0x10)
    data.extend(fatbData)
    data.extend(fntbData)
    data.extend(fimgData)
    _common.NDS_STD_FILE_HEADER.pack_into(
        data, 0, b'NARC', 0xFEFF, 1, len(data), 0x10, 3)
    return bytes(data)


def saveToFile(filenames, fileList, filePath):
    """
    Create a NARC archive from a filename table and a list of files, and
    save it to a filesystem file.
    """
    d = save(filenames, fileList)
    with open(filePath, 'wb') as f:
        f.write(d)
