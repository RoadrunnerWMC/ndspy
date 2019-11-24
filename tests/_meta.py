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
Utilities for writing the tests themselves.
"""

def niceBytesRepr(data, breakEvery=8):
    """
    Like bytes.__repr__(), but uses the abbreviated \\N octal notation,
    and splits it up into new literals separated by linebreaks every
    breakEvery bytes.

    Based on shortBytesRepr() from ndspy._common
    """

    def makePart(data):
        r = ["b'"]
        for i, b in enumerate(data):
            if breakEvery is not None and i != 0 and i % breakEvery == 0:
                r.append("'\nb'")
            if b < 8 and (i == len(data) - 1 or data[i + 1] not in range(0x30, 0x3A)):
                r.append(f'\\{b}')
            elif b in range(0x30, 0x3A) or b in range(0x41, 0x5B) or b in range(0x61, 0x7B):
                r.append(repr(b.to_bytes(1, 'big'))[2:-1])
            else:
                r.append(f'\\x{b:02x}')
        r.append("'")
        return r

    r = []
    for i in range(len(data) // breakEvery):
        r.extend(makePart(data[i * breakEvery : i * breakEvery + breakEvery]))
        r.append('\n')
    r.pop()

    return ''.join(r)
