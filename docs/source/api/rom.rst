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

``ndspy.rom``: ROMs
===================

.. py:module:: ndspy.rom

``ndspy.rom`` provides a class that represents a Nintendo DS ROM file.

.. note::
    
    Unlike most ndspy documentation, the attributes of
    :py:class:`NintendoDSRom` aren't arranged mostly alphabetically. Rather,
    they're sorted in the same order as in ROM header data.


Examples
--------

Change a ROM's name and resave it:

.. code-block:: python

    >>> import ndspy.rom
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')
    >>> print(rom.name)
    bytearray(b'NEW MARIO')
    >>> rom.name = b'Example Name'
    >>> rom.saveToFile('nsmb_edited.nds')
    >>>

Get a file from a ROM by file ID:

.. code-block:: python

    >>> import ndspy.rom
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')
    >>> soundDataSDAT = rom.files[134]
    >>> with open('sound_data.sdat', 'wb') as f:
    ...     f.write(soundDataSDAT)
    ...
    4839008
    >>>

Replace a file in a ROM by filename, and resave it:

.. code-block:: python

    >>> import ndspy.rom
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')
    >>> with open('sound_data.sdat', 'rb') as f:
    ...     soundDataSDAT = f.read()
    ...
    >>> rom.setFileByName('sound_data.sdat', soundDataSDAT)
    >>> rom.saveToFile('nsmb_edited.nds')
    >>>

Print the names of all NSBTX files, found by looking for their file data magics
rather than file extensions:

.. code-block:: python

    >>> import ndspy.rom
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')
    >>> rom.setFileByName('sound_data.sdat', soundDataSDAT)
    >>> for i, file in enumerate(rom.files):
    ...     if file.startswith(b'BTX0'):
    ...         print(rom.filenames.filenameOf(i))
    ...
    enemy/b_lift.nsbtx
    enemy/d_bridge.nsbtx
    enemy/I_do_hahen_l.nsbtx
    enemy/I_do_hahen_r.nsbtx
    enemy/I_kaiten_ami.nsbtx
    [snip]
    polygon_unit/wire_netting8.nsbtx
    polygon_unit/wire_netting9.nsbtx
    >>>

Load a ROM's ARM9 code file and overlays:

.. code-block:: python

    >>> arm9 = rom.loadArm9()
    >>> print(arm9)
    <main-code at 0x02000000
        <code-section at 0x02000000: b'\xff\xde\xff\xe7\xff\xde\xff\xe7\xff\xde\xff\xe7\xff\xde\x15\xa3\x82\xe5\x1d\1\xfa\x11\x1c%\x8a\td\x80\x19\xaf\xdc\x8d'... implicit>
        <code-section at 0x01FF8000: b'\0\xc0\x90\xe5\40\x90\xe5H \x9f\xe5H\x10\x9f\xe5\0\xc0\x82\xe5\40\x82\xe5\x08\xc0\x90\xe5\x0c \x90\xe5'...>
        <code-section at 0x027E0000: b'`\x81\xff\1`\x81\xff\1`\x81\xff\18\x83\xff\1H\x83\xff\1X\x83\xff\1h\x83\xff\1`\x81\xff\1'...>
        <code-section at 0x02043380: b'\0\x10\x90\xe5\0\0Q\xe3\1\x10A\x12\0\x10\x80\x15\0\0\x90\xe5\x1e\xff/\xe1\xb0\x10\xd0\xe1\0\0Q\xe3'...>
        <code-section at 0x02085880: b''>
    >
    >>> overlays = rom.loadArm9Overlays()
    >>> for id, overlay in overlays.items():
    ...     print(id, overlay)
    ...
    0 <overlay at 0x020986E0 file=0 compressed verify-hash>
    1 <overlay at 0x020CC2E0 file=5 compressed verify-hash>
    2 <overlay at 0x020CC2E0 file=7 compressed verify-hash>
    3 <overlay at 0x020CC2E0 file=9 compressed verify-hash>
    4 <overlay at 0x020CC2E0 file=11 compressed verify-hash>
    5 <overlay at 0x020CC2E0 file=12 compressed verify-hash>
    [snip]
    129 <overlay at 0x020B8920 file=27 compressed verify-hash>
    130 <overlay at 0x021226E0 file=126 compressed verify-hash>
    >>>


API
---

.. data:: ICON_BANNER_LEN

    The length (in bytes) of the icon banner data: 0x840.

    .. seealso::

        The class attribute that this measures the length of:
        :py:attr:`NintendoDSRom.iconBanner`.


.. py:class:: NintendoDSRom([data])

    A Nintendo DS ROM file (.nds).

    :param bytes data: The data to be read as a ROM file. If not provided, the
        ROM will use default values.

    .. py:attribute:: name

        The ROM's name. This is usually a short ASCII string containing the
        name of the software. This can be up to 12 bytes long; longer values
        will be truncated when saving.

        This is at offset 0x000 in the ROM header.

        :type: :py:class:`bytes` (12-byte limit)

        :default: ``b''``

    .. py:attribute:: idCode

        The four-byte ID code of the software. Usually, this is ASCII, and the
        fourth character is a region identifier ("E" for North America, "P" for
        Europe, or "J" for Japan).

        This is at offset 0x00C in the ROM header.

        :type: :py:class:`bytes` (exactly 4 bytes long)

        :default: ``b'####'``

    .. py:attribute:: developerCode

        An identifier for the developer of the software. Usually two ASCII
        characters; for example, Nintendo is "01".

        This is at offset 0x010 in the ROM header.

        :type: :py:class:`bytes` (exactly 2 bytes long)

        :default: ``b'\0\0'``

    .. py:attribute:: unitCode

        The systems this ROM supports:

        * 0: Nintendo DS (DSi only in compatibility mode)
        * 2: Both Nintendo DS and Nintendo DSi
        * 3: Nintendo DSi only

        This is at offset 0x012 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: encryptionSeedSelect

        The seed number to use when decrypting the ROM. The actual seed values
        are built into the DS's hardware; this is only an index into a table.
        Valid values are 0 through 7, inclusive.

        This is at offset 0x013 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: deviceCapacity

        A number representing the storage capacity of the hardware this ROM is
        intended to be placed on. The formula is ``2 ^ (17 + X)`` bytes; for
        example, a value of 7 means 16 MB.

        This is at offset 0x014 in the ROM header.

        .. note::

            This can optionally be recalculated for you automatically upon
            saving the ROM. For more information about this, see the
            documentation for the :py:func:`save` function.

        :type: :py:class:`int`

        :default: 9

    .. py:attribute:: pad015

        The value of the padding byte at 0x015 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad016

        The value of the padding byte at 0x016 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad017

        The value of the padding byte at 0x017 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad018

        The value of the padding byte at 0x018 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad019

        The value of the padding byte at 0x019 in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad01A

        The value of the padding byte at 0x01A in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad01B

        The value of the padding byte at 0x01B in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad01C

        The value of the padding byte at 0x01C in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: region

        The region this ROM is intended to be used in:

        * 0x00: most regions
        * 0x40: Korea
        * 0x80: China

        This is at offset 0x01D in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: version

        The version number for this ROM. It's unclear exactly what this means.

        This is at offset 0x01E in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: autostart

        A value related to how the ROM should be loaded. If
        ":py:attr:`autostart` & 4" is set, the "Press Button" message after the
        Health and Safety screen will be skipped.

        This is at offset 0x01F in the ROM header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: arm9EntryAddress

        The RAM address that ARM9 execution should begin at, after the ARM9
        code has been loaded into RAM at :py:attr:`arm9RamAddress`.

        This is at offset 0x024 in the ROM header.

        .. seealso::

            :py:attr:`arm9` -- the code data that this entry address should
            reference.

        :type: :py:class:`int`

        :default: 0x02000800

    .. py:attribute:: arm9RamAddress

        The RAM address that the ARM9 code should be loaded to.

        This is at offset 0x028 in the ROM header.

        .. seealso::

            :py:attr:`arm9` -- the code data that will be loaded to this
            address.

        :type: :py:class:`int`

        :default: 0x02000000

    .. py:attribute:: arm7EntryAddress

        The RAM address that ARM7 execution should begin at, after the ARM7
        code has been loaded into RAM at :py:attr:`arm7RamAddress`.

        This is at offset 0x034 in the ROM header.

        .. seealso::

            :py:attr:`arm7` -- the code data that this entry address should
            reference.

        :type: :py:class:`int`

        :default: 0x02380000

    .. py:attribute:: arm7RamAddress

        The RAM address that the ARM7 code should be loaded to.

        This is at offset 0x038 in the ROM header.

        .. seealso::

            :py:attr:`arm7` -- the code data that will be loaded to this
            address.

        :type: :py:class:`int`

        :default: 0x02380000

    .. py:attribute:: normalCardControlRegisterSettings

        The "port 0x040001A4 setting for normal commands". For more
        information, see `the section about this value on GBATEK
        <http://problemkaputt.de/gbatek.htm#dscartridgeioports>`__
        (subheader "40001A4h - NDS7/NDS9 - ROMCTRL - Gamecard Bus ROMCTRL
        (R/W)").

        This is at offset 0x060 in the ROM header.

        :type: :py:class:`int`

        :default: 0x00416657

    .. py:attribute:: secureCardControlRegisterSettings

        The "port 0x040001A4 setting for KEY1 commands". For more information,
        see `the section about this value on GBATEK
        <http://problemkaputt.de/gbatek.htm#dscartridgeioports>`__
        (subheader "40001A4h - NDS7/NDS9 - ROMCTRL - Gamecard Bus
        ROMCTRL (R/W)").

        This is at offset 0x064 in the ROM header.

        :type: :py:class:`int`

        :default: 0x081808f8

    .. py:attribute:: secureAreaChecksum

        The checksum of the encrypted "secure area" of the ROM.

        This is at offset 0x06C in the ROM header.

        .. todo::

            This should be calculated automatically when saving the ROM instead
            of being an attribute.

        :type: :py:class:`int`

        :default: 0x0000

    .. py:attribute:: secureTransferDelay

        A delay value of some kind related to encryption commands. Measured in
        units of 130.912kHz each. For more information, see `the section about
        this value on GBATEK
        <http://problemkaputt.de/gbatek.htm#dscartridgeheader>`__ (subheader
        "Secure Area Delay").

        This is at offset 0x06E in the ROM header.

        :type: :py:class:`int`

        :default: 0x0D7E

    .. py:attribute:: arm9CodeSettingsPointerAddress

        The address in RAM (plus 4) of a pointer to the "code settings"
        structure in ARM9's main code file. This defines things like the SDK
        version used to compile the ROM, whether the code is compressed or not,
        and the list of ARM9 code "sections" and where they should be placed in
        memory. If this value is 0, then either there is no code settings block
        in ARM9 or its location is unspecified.

        This is at offset 0x070 in the ROM header.

        .. note::
            You have to subtract 4 from this value to get the actual address of
            the pointer to the code settings block.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: arm7CodeSettingsPointerAddress

        The address in RAM (plus 4) of a pointer to the "code settings"
        structure in ARM7's main code file. This defines things like the SDK
        version used to compile the ROM, whether the code is compressed or not,
        and the list of ARM7 code "sections" and where they should be placed in
        memory. If this value is 0, then either there is no code settings block
        in ARM7 or its location is unspecified.

        This is at offset 0x074 in the ROM header.

        .. note::
            You have to subtract 4 from this value to get the actual address of
            the pointer to the code settings block.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: secureAreaDisable

        This value disables the encrypted "secure area" of the ROM, allowing
        one to use that area without encryption. To do this, the value must be
        set to "NmMdOnly", encrypted. This is probably impossible without
        Nintendo's private keys.

        This is at offset 0x078 in the ROM header.

        :type: :py:class:`bytes` (exactly 8 bytes long)

        :default: ``b'\0\0\0\0\0\0\0\0'``

    .. py:attribute:: pad088

        Padding area beginning at 0x088 in the ROM header.

        :type: :py:class:`bytes` (exactly 0x38 bytes long)

        :default: ``b'\0' * 0x38``

    .. py:attribute:: nintendoLogo

        A compressed image of the Nintendo logo. The DS will refuse to load the
        ROM if this is modified in any way.

        This is at offset 0x0C0 in the ROM header.

        :type: :py:class:`bytes` (exactly 0x9C bytes long)

        :default: (the correct value)

    .. py:attribute:: debugRomAddress

        The address where the "debug rom" should be loaded to in RAM, if
        present. It's unclear what exactly this is.

        This is at offset 0x168 in the ROM header.

        .. seealso::

            :py:attr:`debugRom` -- the data this refers to.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pad16C

        Padding area beginning at 0x16C in the ROM header.

        :type: :py:class:`bytes` (exactly 0x94 bytes long)

        :default: ``b'\0' * 0x94``

    .. py:attribute:: pad200

        Padding after the ROM header, beginning at 0x200.

        :type: :py:class:`bytes`

        :default: ``b'\0' * 0x3E00``

    .. py:attribute:: rsaSignature

        The ROM's RSA signature data. Not every ROM has is cryptographically
        signed, but for those that are, this is stored at the very end of the
        ROM. Since most methods of playing games from ROM files these days
        bypass the RSA verification step, this attribute probably isn't very
        useful for most purposes.

        :type: :py:class:`bytes` (either 0 or 0x88 bytes long)

        :default: ``b''``

    .. py:attribute:: arm9

        The main ARM9 executable binary to be loaded to
        :py:attr:`arm9RamAddress`.

        .. seealso::

            :py:class:`ndspy.code.MainCodeFile` -- the ndspy class you can use
            to load this data.

            :py:attr:`arm9RamAddress` -- the address this will be loaded to in
            RAM.

            :py:attr:`arm9EntryAddress` -- the address in RAM where ARM9
            execution will begin.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: arm9PostData

        A small amount of extra data immediately following :py:attr:`arm9` in
        the ROM data. It is unclear what this is for.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: arm7

        The main ARM7 executable binary to be loaded to
        :py:attr:`arm7RamAddress`.

        .. seealso::

            :py:class:`ndspy.code.MainCodeFile` -- the ndspy class you can use
            to load this data.

            :py:attr:`arm7RamAddress` -- the address this will be loaded to in
            RAM.

            :py:attr:`arm7EntryAddress` -- the address in RAM where ARM7
            execution will begin.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: arm9OverlayTable

        The table containing information about ARM9 overlays.

        .. seealso::

            :py:func:`ndspy.code.loadOverlayTable` -- the ndspy function you
            can use to load this data.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: arm7OverlayTable

        The table containing information about ARM7 overlays.

        .. seealso::

            :py:func:`ndspy.code.loadOverlayTable` -- the ndspy function you
            can use to load this data.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: iconBanner

        A structure containing the game's icon data, and its title in multiple
        languages. For more information, see `the section about this value on
        GBATEK <http://problemkaputt.de/gbatek.htm#dscartridgeicontitle>`__.

        .. seealso::

            :py:const:`ICON_BANNER_LEN` -- a constant containing the length of
            this data (0x840).

        :type: :py:class:`bytes` (exactly 0x840 bytes long).

        :default: ``b''``

    .. py:attribute:: debugRom

        Some optional data related to debugging; it's unclear what exactly this
        is.

        .. seealso::

            :py:attr:`debugRomAddress` -- the address in RAM this will be
            loaded to.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: filenames

        The root folder of the ROM's filename table. These filenames usually do
        not cover all files in the ROM (for example, overlays are usually
        unnamed).

        .. seealso::

            :py:mod:`ndspy.fnt` -- the ndspy module the
            :py:class:`ndspy.fnt.Folder` class resides in.

            :py:attr:`files` -- the corresponding list of files that these
            filenames refer to.

        :type: :py:class:`ndspy.fnt.Folder`

        :default: ``ndspy.fnt.Folder()``

    .. py:attribute:: files

        The list of files in this ROM. Indices are file IDs; that is,
        ":py:attr:`files`\[0]" is the file with file ID 0,
        ":py:attr:`files`\[1]" is the file with file ID 1, etc.

        .. seealso::

            :py:attr:`filenames` -- the set of filenames for these files.

        :type: :py:class:`list` of :py:class:`bytes`

        :default: ``[]``

    .. py:attribute:: sortedFileIds

        For unknown reasons, ROMs sometimes store files in an order other than
        that of ascending file IDs. To preserve this order, this list contains
        file IDs in the order in which they should be saved in the ROM data.
        This is automatically populated when opening a ROM, and you should
        never really need to change this. (You can empty it to force files to
        be saved in order, though.)

        If any file IDs are missing from this list, they will be placed in
        order of ascending file IDs after the files that are in the list. If
        this is empty, all files will be saved in order of ascending file IDs. 

        .. seealso::

            :py:attr:`files` -- the list of files these indices refer to.

        :type: :py:class:`list` of :py:class:`int`

        :default: ``[]``

    .. py:classmethod:: fromFile(filePath)

        Load a ROM from a filesystem file. This is a convenience function.

        :param filePath: The path to the ROM file to open.
        :type filePath: :py:class:`str` or other path-like object

        :returns: The ROM object.
        :rtype: :py:class:`NintendoDSRom`

    .. py:function:: getFileByName(filename)

        Return the data for the file with the given filename (path). This is a
        convenience function; the following two lines of code are exactly
        equivalent (apart from some error checking):

        .. code-block:: python

            fileData = rom.getFileByName(filename)
            fileData = rom.files[rom.filenames.idOf(filename)]

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

            rom.setFileByName(filename, fileData)
            rom.files[rom.filenames.idOf(filename)] = fileData

        .. seealso::
            :py:func:`getFileByName` -- to retrieve the file data
            instead of replacing it.

        :param str filename: The name of the file.
        :param bytes data: The new data for the file.

    .. py:function:: loadArm7()

        Create a :py:class:`ndspy.code.MainCodeFile` object representing the
        main ARM7 code file in this ROM.

        .. seealso::
            :py:attr:`arm7` -- depending on what you're trying to do, it may be
            more appropriate to just use this raw data attribute directly
            instead.

        :returns: The ARM7 code file.
        :rtype: :py:class:`ndspy.code.MainCodeFile`

    .. py:function:: loadArm7Overlays([idsToLoad])

        Create a dictionary of this ROM's ARM7
        :py:class:`ndspy.code.Overlay`\s.

        .. seealso::
            :py:attr:`arm7OverlayTable` -- if you just want the raw overlay
            table data, you can access it from this attribute instead. This
            avoids the side effect of decompressing all of the overlay data
            (which can be slow).

        :param idsToLoad: A specific set of overlay IDs to load. You can use
            this to avoid loading overlays you don't actually care about, in
            order to improve your application's performance.
        :type idsToLoad: :py:class:`set` of :py:class:`int`

        :returns: A :py:class:`dict` of overlays.
        :rtype: :py:class:`dict`: ``{overlayID: overlay}`` (where ``overlayID``
            is of type :py:class:`int` and ``overlay`` is of type
            :py:class:`Overlay`)

    .. py:function:: loadArm9()

        Create a :py:class:`ndspy.code.MainCodeFile` object representing the
        main ARM9 code file in this ROM.

        .. seealso::
            :py:attr:`arm9` -- depending on what you're trying to do, it may be
            more appropriate to just use this raw data attribute directly
            instead.

        :returns: The ARM9 code file.
        :rtype: :py:class:`ndspy.code.MainCodeFile`

    .. py:function:: loadArm9Overlays([idsToLoad])

        Create a dictionary of this ROM's ARM9
        :py:class:`ndspy.code.Overlay`\s.

        .. seealso::
            :py:attr:`arm9OverlayTable` -- if you just want the raw overlay
            table data, you can access it from this attribute instead. This
            avoids the side effect of decompressing all of the overlay data
            (which can be slow).

        :param idsToLoad: A specific set of overlay IDs to load. You can use
            this to avoid loading overlays you don't actually care about, in
            order to improve your application's performance.
        :type idsToLoad: :py:class:`set` of :py:class:`int`

        :returns: A :py:class:`dict` of overlays.
        :rtype: :py:class:`dict`: ``{overlayID: overlay}`` (where ``overlayID``
            is of type :py:class:`int` and ``overlay`` is of type
            :py:class:`Overlay`)

    .. py:function:: save(*[, updateDeviceCapacity=False])

        Generate file data representing this ROM.

        :param bool updateDeviceCapacity: If this is ``True``,
            :py:attr:`deviceCapacity` will be updated based on the size of the
            output file data. It will be set to match the capacity of the
            smallest cartridge that would be able to hold the data.

            :default: ``False``

        :returns: The ROM file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath, *[, updateDeviceCapacity=False])

        Generate file data representing this ROM, and save it to a filesystem
        file. This is a convenience function.

        :param filePath: The path to the ROM file to save to.
        :type filePath: :py:class:`str` or other path-like object

        :param bool updateDeviceCapacity: If this is ``True``,
            :py:attr:`deviceCapacity` will be updated based on the size of the
            output file data. It will be set to match the capacity of the
            smallest cartridge that would be able to hold the data.

            :default: ``False``
