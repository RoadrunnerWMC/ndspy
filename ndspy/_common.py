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


import struct

import crcmod


# Nintendo DS standard file header:
NDS_STD_FILE_HEADER = struct.Struct('<4sHHIHH')
# - Magic
# - BOM
# - Version (generally 1)
# - File size (including this header)
# - Size of this header (16)
# - Number of blocks


def crc16(data):
    return crcmod.predefined.mkCrcFun('modbus')(data)


def loadNullTerminatedStringFrom(
        data, offset, charWidth=1, encoding='latin-1'):
    """
    Load a null-terminated string from data at offset, with the options
    given
    """
    end = data.find(b'\0' * charWidth, offset)
    return data[offset:end].decode(encoding)


def listFind(L, *args):
    try:
        return L.index(*args)
    except ValueError:
        return -1


def noteName(value):
    note = value - 60
    letter = 'ccddeffggaab'[note % 12]
    sharp  = ' ♯ ♯  ♯ ♯ ♯ '[note % 12].strip()
    if note < -12:
        letter = letter.upper()
    accents = ''
    while note >= 0:
        accents += "'"
        note -= 12
    while note < -24:
        accents += '͵'
        note += 12
    return letter + sharp + accents


def isIterable(object):
    """
    Check whether an object is iterable or not.
    """
    # https://stackoverflow.com/a/1952481
    try:
        iter(object)
        return True
    except TypeError:
        return False


def shortBytesRepr(data):
    """
    Like bytes.__repr__(), but will truncate large amounts of data.
    Will also take advantage of octal encoding to make the output more
    compact.
    """
    MAX_LEN = 0x20

    dataTrunc = data[:MAX_LEN]
    r = ["b'"]
    for b in dataTrunc:
        if b < 8:
            r.append(f'\\{b}')
        else:
            r.append(repr(bytes([b]))[2:-1])
    r.append("'")

    final = ''.join(r)

    if len(data) > MAX_LEN:
        return final + '...'
    else:
        return final


def shortColorsListRepr(colors):
    """
    Like shortBytesRepr(), but for lists of colors.
    """
    MAX_COLORS = 20
    colorsTrunc = colors[:MAX_COLORS]
    hexColors = (f'0x{c:04X}' for c in colorsTrunc)
    ellipsis = ', ...' if len(colors) > MAX_COLORS else ''
    return f'[{", ".join(hexColors)}{ellipsis}]'


def loadInfoBlock(data, off, expectedEntryLengths=None):
    """
    Read an info block.
    These are used extensively in NSBMD and NSBTX files.
    """

    # Read overall header
    count, infoBlockSize = struct.unpack_from('<xBH', data, off)
    off += 4

    # Read unk block header and get array pointer
    unkHeaderLen, unkLen, unkUnk04 = \
        struct.unpack_from('<HHI', data, off)
    off += 8
    assert unkHeaderLen == 8
    assert unkLen == 12 + 4 * count
    assert unkUnk04 == 0x17F
    unkBlockOff = off
    off += 4 * count

    # Read entries block header and get array pointer
    eachEntryLen, entriesLen = \
        struct.unpack_from('<HH', data, off)
    if expectedEntryLengths is not None:
        assert eachEntryLen == expectedEntryLengths
    assert entriesLen == 4 + count * eachEntryLen
    off += 4
    entryOff = off
    off += eachEntryLen * count

    # Get names array pointer
    nameOff = off

    # Gather entries into a list
    entries = []
    for i in range(count):
        unk00, unk02 = struct.unpack_from('<HH', data, unkBlockOff)
        entry = data[entryOff : entryOff+eachEntryLen]
        name = data[nameOff : nameOff+16].rstrip(b'\0').decode('latin-1')

        entries.append((name, unk00, unk02, entry))

        unkBlockOff += 4
        entryOff += eachEntryLen
        nameOff += 16

    return entries


def saveInfoBlock(entries, entryLengths):
    """
    The inverse of loadInfoBlock().
    entryLengths is required, so the code can properly handle the case
    of a completely empty entries list.
    """
    data = bytearray()

    # Create the overall header
    # (overall size value will be inserted at the end)
    data.extend(struct.pack('<xBH', len(entries), 0))

    # Write the unk block
    data.extend(struct.pack('<HHI', 8, 12 + 4 * len(entries), 0x17F))
    for e in entries:
        data.extend(struct.pack('<HH', e[1], e[2]))

    # Write the entries block
    data.extend(struct.pack('<HH', entryLengths, 4 + len(entries) * entryLengths))
    for e in entries:
        if len(e[3]) != entryLengths:
            raise ValueError('One of the entries is not of length'
                f' {entryLengths} like it should be'
                f' (actual length is {len(e[3])})')
        data.extend(e[3])

    # Write the names block
    for e in entries:
        if e[0] is None:
            data.extend(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
        else:
            data.extend(e[0].encode('latin-1').ljust(16, b'\0'))

    # Insert the overall size, now that we know what it is
    struct.pack_into('<H', data, 2, len(data))

    return bytes(data)
