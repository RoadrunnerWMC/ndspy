..
    Copyright 2019 RoadrunnerWMC

    This file is part of ndspy.

    ndspy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ndspy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ndspy.  If not, see <https://www.gnu.org/licenses/>.

``ndspy.codeCompression``: Code Compression
===========================================

.. py:module:: ndspy.codeCompression

``ndspy.codeCompression`` provides functions for the compression format used
for executable code files. (This is essentially the same as LZ10 compression,
except that the file is decompressed in reverse, beginning at the end of the
file. This allows for in-place decompression, which is more efficient.)

.. note::
    If you're using the :py:mod:`ndspy.code` module, compression is handled
    automatically for you, and you shouldn't need to use this module
    explicitly.


.. py:function:: compress(data[, isArm9=False])

    Compress code data. This is the inverse of :py:func:`decompress`.

    :param bytes data: The data to compress.

    :param bool isArm9: Whether the data to be compressed is a main ARM9 code
        file or not. ARM9 code needs to be compressed slightly differently.
        (This should be ``False`` for overlays.)

        :default: ``False``

    :returns: The compressed data.
    :rtype: :py:class:`bytes`


.. py:function:: decompress(data)

    Decompress data that was compressed using code compression. This is the
    inverse of :py:func:`compress`.

    If the data does not seem to be compressed, it will be returned unmodified.

    :param bytes data: The compressed data.

    :returns: The decompressed data.
    :rtype: :py:class:`bytes`
