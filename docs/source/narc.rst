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

``ndspy.narc``: NARC Archives
=============================

.. py:module:: ndspy.narc

The ``ndspy.narc`` module allows you to open and save *NARC* archive files.

*NARC* archives are structured similarly to ROM files, in that each file can be
referenced by either ID or by a filename from a filename table. Filename tables
work the same as those of ROMs.


Examples
--------

Load a *NARC* from a loose file and see what's inside:

.. code-block:: python

    >>> import ndspy.narc
    >>> narc = ndspy.narc.NARC.fromFile('mg_trampoline.narc')
    >>> print(narc)
    <narc endiannessOfBeginning='>'
        0000 mg_trampoline/
        0000     d_2d_mg_bg_trampoline_nsc.bin       b'\x10\0\x10\0-~\xc2\xf0\1\xa4\xf0\x13\xe0%\xa5@'...
        0001     d_2d_mgvs_bg_trampoline_ncg.bin     b'\x10\04\0\0(\xb5\xbbu(\xb5\x8bv\0(\x98'...
        0002     d_2d_mgvs_bg_trampoline_ncl.bin     b'\xc87\xcb]\xece-nnv\0\0\0\0\0\0'...
        0003     d_2d_mgvs_bg_trampoline_nsc.bin     b'\x10\0\x10\0\0\0\xf3\1\xf3\2\xf3~\xc2\0~\xc2'...
        0004     d_2d_mgvs_trampoline_ncl.bin        b'9W\0\0\0\0\xff\x7f:\x1e\xbb2|O-\4'...
        0005     US/
        0005         d_2d_mgvs_trampoline_ncg.bin    b'\x10\0\x18\0\0\0\0\x10\x11\0\0\x113\1\0\x10'...
    >
    >>>

Load a *NARC* from within a ROM, replace a file, and save it back into the ROM:

.. code-block:: python

    >>> import ndspy.rom, ndspy.narc
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('Zelda - Phantom Hourglass.nds')
    >>> narc = ndspy.narc.NARC(rom.getFileByName('Effect/effecttex.narc'))
    >>> print(narc)
    <narc endiannessOfBeginning='>'
        0000 AK_smoke01.ntfi     b'\0@\0@\0@\0@\0@\0@\0@\0@'...
        0001 AK_smoke01.ntfp     b'\0\0\0\0\xbdw\0\0\xff\x7f\0\0c\x0c\0\0'...
        0002 AK_smoke01.ntft     b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'...
        0003 AK_smoke02.ntfi     b'\0@\0@\0@\0@\0@\0@\0@\0@'...
        0004 AK_smoke02.ntfp     b'\0\0\0\0\xde{\0\0\xff\x7f!\4\xe7\x1c\0\0'...
        0005 AK_smoke02.ntft     b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'...
        0006 AK_smoke03.ntfi     b'\0@\0@\0@\0@\0@\0@\0@\0@'...
        0007 AK_smoke03.ntfp     b'\0\0\0\0\xd6Z\0\0{o\0\0\xde{\0\0'...
        0008 AK_smoke03.ntft     b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'...
        0009 smoke01.ntfi        b'\0@\0@\0@\0@\0@\0@\0@\0@'...
        0010 smoke01.ntfp        b'\0\0\0\0\xde{\0\0\xff\x7f\x84\x10\xff\x7f\0\0'...
        0011 smoke01.ntft        b'\xff\xff\xff\xff\xff\xff\xff?\xff\xff\xff\0\xff\xff\xff\0'...
        0012 smoke02.ntfi        b'\0@\0@\0@\1@\2@\3@\4@\0@'...
        0013 smoke02.ntfp        b'\xe7\x1c\0\0{o\0\0\x9cs\0\0J)\0\0'...
        0014 smoke02.ntft        b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff_\x15\xffWU\2'...
        0015 smoke03.ntfi        b'\0@\0@\0@\0@\0@\0@\0@\0@'...
        0016 smoke03.ntfp        b'\0\0\0\0\xde{\0\0\xff\x7f\xc6\x18\xff\x7fc\x0c'...
        0017 smoke03.ntft        b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\3'...
        0018 zds_airflow.ntfp    b'\0\0\xff\x7f'
        0019 zds_airflow.ntft    b'\0\0@UU\1\0\0\0@UUUU\1\0'...
    >
    >>> narc.setFileByName('zds_airflow.ntfp', b'example data of some kind')
    >>> rom.setFileByName('Effect/effecttex.narc', narc.save())
    >>> rom.saveToFile('Zelda - Phantom Hourglass - Edited.nds')
    >>>

Create a new *NARC* from scratch, and save it to a file:

.. code-block:: python

    >>> import ndspy.narc, ndspy.fnt
    >>> with open('a.txt', 'rb') as f:
    ...    aTxt = f.read()
    ...
    >>> with open('b.bin', 'rb') as f:
    ...    bBin = f.read()
    ...
    >>> with open('images/c.png', 'rb') as f:
    ...    cPng = f.read()
    ...
    >>> root = ndspy.fnt.Folder(files=['a.txt', 'b.bin'])
    >>> imagesFolder = ndspy.fnt.Folder(files=['c.png'])
    >>> # a.txt and b.bin come before the images/ folder. Thus, they'll have
    ... # IDs 0 and 1, and the images/ folder therefore needs ID 2:
    ...
    >>> imagesFolder.firstID = 2
    >>> root.folders = [('images', imagesFolder)]
    >>> narc = ndspy.narc.NARC.fromFilesAndNames([aTxt, bBin, cPng], root)
    >>> print(narc)
    <narc
        0000 a.txt        b'Contents of a.tx'...
        0001 b.bin        b'Contents of b.bi'...
        0002 images/
        0002     c.png    b'\x89PNG\r\n\x1a\n\0\0\0\rIHDR'...
    >
    >>> narc.saveToFile('things.narc')
    >>>


API
---

.. py:class:: NARC([data])

    A *NARC* archive file.

    :param data: The data to be read as a *NARC* file. If this is not provided,
        the *NARC* object will initially be empty.
    :type data: bytes

    .. py:attribute:: endiannessOfBeginning

        The endianness of the first 8 bytes of the *NARC* file header. The rest
        of the file is always little-endian.

        ``'<'`` and ``'>'`` (representing little-endian and big-endian,
        respectively) are the only values this attribute is allowed to take.

        :type: :py:class:`str`

        :default: ``'<'``

    .. py:attribute:: filenames

        The root folder of the *NARC*'s filename table.

        .. seealso::

            :py:mod:`ndspy.fnt` -- the ndspy module the
            :py:class:`ndspy.fnt.Folder` class resides in.

            :py:attr:`files` -- the corresponding list of files that these
            filenames refer to.

        :type: :py:class:`ndspy.fnt.Folder`

        :default: ``ndspy.fnt.Folder()``

    .. py:attribute:: files

        The list of files in this *NARC*. Indices are file IDs; that is,
        ":py:attr:`files`\[0]" is the file with file ID 0,
        ":py:attr:`files`\[1]" is the file with file ID 1, etc.

        .. seealso::

            :py:attr:`filenames` -- the set of filenames for these files.

        :type: :py:class:`list` of :py:class:`bytes`

        :default: ``[]``

    .. py:classmethod:: fromFilesAndNames(files[, filenames])

        Create a *NARC* archive from a list of files and (optionally) a
        filename table.

        :param files: The initial value for the :py:attr:`files` attribute.

        :param filenames: The initial value for the :py:attr:`filenames`
            attribute.

        :returns: The *NARC* object.
        :rtype: :py:class:`NARC`

    .. py:classmethod:: fromFile(filePath)

        Load a *NARC* archive from a filesystem file. This is a convenience
        function.

        :param filePath: The path to the *NARC* file to open.
        :type filePath: :py:class:`str` or other path-like object

        :returns: The *NARC* object.
        :rtype: :py:class:`NARC`

    .. py:function:: getFileByName(filename)

        Return the data for the file with the given filename (path). This is a
        convenience function; the following two lines of code are exactly
        equivalent (apart from some error checking):

        .. code-block:: python

            fileData = narc.getFileByName(filename)
            fileData = narc.files[narc.filenames.idOf(filename)]

        .. seealso::
            :py:func:`setFileByName` -- to replace the file data instead of
            retrieving it.

        :param str filename: The name of the file.

        :returns: The file's data.
        :rtype: :py:class:`bytes`

    .. py:function:: setFileByName(filename, data)

        Replace the data for the file with the given filename (path) with the
        given data. This is a convenience function; the following two lines of
        code are exactly equivalent (apart from some error checking):

        .. code-block:: python

            narc.setFileByName(filename, fileData)
            narc.files[narc.filenames.idOf(filename)] = fileData

        .. seealso::
            :py:func:`getFileByName` -- to retrieve the file data
            instead of replacing it.

        :param str filename: The name of the file.
        :param bytes data: The new data for the file.

    .. py:function:: save()

        Generate file data representing this *NARC*.

        :returns: The *NARC* archive file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *NARC*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *NARC* archive file to save to.
        :type filePath: :py:class:`str` or other path-like object
