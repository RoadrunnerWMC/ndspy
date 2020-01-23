..
    Copyright 2020 RoadrunnerWMC

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

:py:mod:`ndspy.codeCompression`'s command-line interface allows you to easily
compress and decompress files using the compression format used for NDS
executable code files. You can access it through
``python3 -m ndspy.codeCompression`` or ``ndspy_codeCompression``, or
programmatically with :py:func:`ndspy.codeCompression.main`.

Usage summary:

.. code-block:: text

    $ python3 -m ndspy.codeCompression -h
    usage: codeCompression.py [-h] {compress,c,decompress,d} ...

    ndspy.codeCompression CLI: Compress or decompress files using the code
    compression format.

    optional arguments:
      -h, --help            show this help message and exit

    commands:
      (run a command with -h for additional help)

      {compress,c,decompress,d}
        compress (c)        compress a file
        decompress (d)      decompress a file

The module provides commands for compression and decompression:


Compress (``compress`` / ``c``)
-------------------------------

Usage summary:

.. code-block:: text

    $ python3 -m ndspy.codeCompression compress -h
    usage: codeCompression.py compress [-h] [--is_arm9] input_file [output_file]

    positional arguments:
      input_file   input file to compress
      output_file  what to save the compressed file as

    optional arguments:
      -h, --help   show this help message and exit
      --is_arm9    treat the data as a main ARM9 code file (do not use for
                   overlays)

This command compresses a file in the code compression format. If no output
filename is given, it defaults to the input filename, with a ``.cmp``
extension.

The ``--is_arm9`` argument corresponds to the ``isArm9`` argument of the :py:func:`compress() <ndspy.codeCompression.compress>` function.


Decompress (``decompress`` / ``d``)
-----------------------------------

Usage summary:

.. code-block:: text

    $ python3 -m ndspy.codeCompression decompress -h
    usage: codeCompression.py decompress [-h] input_file [output_file]

    positional arguments:
      input_file   input file to decompress
      output_file  what to save the decompressed file as

    optional arguments:
      -h, --help   show this help message and exit

This command decompresses a code-compressed file. If no output filename is
given, it defaults to the input filename, with a ``.dec`` extension.
