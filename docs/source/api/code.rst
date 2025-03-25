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

``ndspy.code``: Code
====================

.. py:module:: ndspy.code

The ``ndspy.code`` module can be used to load and save executable code files:

*   :py:class:`MainCodeFile` can be used to work with ARM7 or ARM9 main code
    files.
*   :py:class:`Overlay` can be used to work with ARM7 or ARM9 code overlays.
*   :py:func:`loadOverlayTable` and :py:func:`saveOverlayTable` can be used to
    load and save ARM7 or ARM9 overlay tables.

.. py:class:: MainCodeFile(data, ramAddress[, codeSettingsPointerAddress])

    Either the main ARM7 code file or the main ARM9 code file. On the console,
    the entire file is loaded into RAM as one big chunk, decompressed (if
    needed), and then immediately executed. Usually, the code begins by moving
    different sections of itself to different addresses. You can access all of
    these sections via the :py:attr:`sections` attribute.

    .. note::

        Since this class tries to parse the code data to some degree to give
        you access to its sections, it automatically decompresses the data (if
        compressed) upon loading it.

    :param bytes data: The data to be read as a code file. If this is ``None``,
        the :py:class:`MainCodeFile` object will initially be empty.

    :param ramAddress: The initial value for the :py:attr:`ramAddress`
        attribute.

    :param codeSettingsPointerAddress: The "code settings pointer address"
        value corresponding to this code file, from the ROM header. ndspy needs
        this to correctly determine :py:attr:`codeSettingsOffs`. If 0 or not
        provided, ndspy will attempt to guess :py:attr:`codeSettingsOffs` for
        you.

    .. py:attribute:: codeSettingsOffs

        The offset in the code data of the "code settings" structure present in
        many code files from retail games. This defines things such as sections
        and whether the code is compressed or not. This should be ``None`` if
        this code file has no code settings structure.

        :type: :py:class:`int`

    .. py:attribute:: ramAddress

        The address this code file will be automatically loaded to when the
        software is booted.

        :type: :py:class:`int`

    .. py:attribute:: sections

        The list of :py:class:`Section`\s in this code file. ndspy has to
        populate this list using heuristics, so it may not always be perfectly
        accurate. Some code files (such as homebrew, mainly) may only have one
        (implicit) section.

        :type: :py:class:`list` of :py:class:`Section`

    .. py:classmethod:: fromCompressed(...)

        Create a main code file from compressed code data.

        This function is a bit outdated, since the default constructor can now
        detect code compression. There is no real reason to use this function
        anymore, and it may be removed at some point.

        Parameters are the same as those of the default constructor.

        :returns: The main code file object.
        :rtype: :py:class:`MainCodeFile`

    .. py:classmethod:: fromSections(sections, ramAddress)

        Create a main code file from a list of sections.

        :param sections: The list of sections to be included in this main code
            file.
        :type sections: :py:class:`list` of :py:class:`Section`

        :param ramAddress: The initial value for the :py:attr:`ramAddress`
            attribute.

        :returns: The main code file object.
        :rtype: :py:class:`MainCodeFile`

    .. py:classmethod:: fromFile(filePath, ramAddress)

        Load a main code file from a filesystem file. This is a convenience
        function.

        :param filePath: The path to the main code file to open.
        :type filePath: :py:class:`str` or other path-like object

        :param ramAddress: The initial value for the :py:attr:`ramAddress`
            attribute.

        :returns: The main code file object.
        :rtype: :py:class:`MainCodeFile`

    .. py:function:: save(*[, compress])

        Generate a :py:class:`bytes` object representing this code file.

        :param bool compress: Whether to compress the code or not. Compression
            is optional for ARM9 code, but ARM7 code should never be
            compressed.

            :default: ``False``

        :returns: The code file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath, *[, compress])

        Generate file data representing this main code file, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the main code file to save to.
        :type filePath: :py:class:`str` or other path-like object

        :param bool compress: Whether to compress the code or not. Compression
            is optional for ARM9 code, but ARM7 code should never be
            compressed.

            :default: ``False``


.. py:class:: MainCodeFile.Section(data, ramAddress, bssSize, *, [implicit=False])

    A single section within an ARM7 or ARM9 code file. Code not technically
    contained within a section defined in the sections table in the code
    settings block is represented as an "implicit" section.

    :param data: The initial value for the :py:attr:`data` attribute.

    :param ramAddress: The initial value for the :py:attr:`ramAddress`
        attribute.

    :param bssSize: The initial value for the :py:attr:`bssSize` attribute.

    :param implicit: The initial value for the :py:attr:`implicit` attribute.

    .. py:attribute:: bssSize

        The size of the `.bss section <https://en.wikipedia.org/wiki/.bss>`_
        for this code section.

        :type: :py:class:`int`

    .. py:attribute:: data

        The code data for this section.

        :type: :py:class:`bytearray`

    .. py:attribute:: implicit

        This is ``True`` if this section is implicitly defined and should be
        excluded from the sections table; ``False`` otherwise.

        The first section of every main code file is implicit; this contains
        the code that parses the sections table and loads (explicit) sections
        defined there to their appropriate RAM addresses.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: ramAddress

        The address where this code section will be placed in memory when
        loaded.

        :type: :py:class:`int`


.. py:class:: Overlay(data, ramAddress, ramSize, bssSize, staticInitStart, staticInitEnd, fileID, compressedSize, flags)

    An ARM7 or ARM9
    `code overlay <https://en.wikipedia.org/wiki/Overlay_(programming)>`_.

    .. note::

        If the ``flags`` parameter indicates the data is compressed (see
        :py:attr:`compressed`), the class constructor will automatically
        decompress it. If you need the original compressed data instead, access
        it directly from your ROM's
        :py:attr:`files <ndspy.rom.NintendoDSRom.files>` list using the
        :py:attr:`fileID` attribute.

    :param data: The initial value for the :py:attr:`data` attribute.

    :param ramAddress: The initial value for the :py:attr:`ramAddress`
        attribute.

    :param ramSize: The initial value for the :py:attr:`ramSize` attribute.

    :param bssSize: The initial value for the :py:attr:`bssSize` attribute.

    :param staticInitStart: The initial value for the
        :py:attr:`staticInitStart` attribute.

    :param staticInitEnd: The initial value for the :py:attr:`staticInitEnd`
        attribute.

    :param fileID: The initial value for the :py:attr:`fileID` attribute.

    :param compressedSize: The initial value for the :py:attr:`compressedSize`
        attribute.

    :param flags: The initial value for the :py:attr:`flags` attribute.

    .. py:attribute:: bssSize

        The size of the `.bss section <https://en.wikipedia.org/wiki/.bss>`_
        for this overlay.

        :type: :py:class:`int`

    .. py:attribute:: data

        The :py:class:`bytearray` object containing the decompressed code for this
        overlay.

    .. py:attribute:: compressed

        Alias property for ":py:attr:`flags` & 1". This is ``True`` if the
        overlay was most recently saved (:py:func:`save`) with compression
        enabled (or -- if it hasn't been saved yet -- if the overlay was
        compressed when it was first loaded), and ``False`` otherwise.

        :type: :py:class:`bool`

    .. py:attribute:: compressedSize

        The size of the overlay's data when compressed. If the overlay is
        uncompressed, this should be equal to the length of the uncompressed
        data.

        :type: :py:class:`int`

    .. py:attribute:: fileID

        The file ID for the file containing the code data for this overlay.

        :type: :py:class:`int`

    .. py:attribute:: flags

        A bitfield (8 bits long) representing some flags for the overlay.
        Values may be game-specific, but known flags have been given named
        aliases.

        :type: :py:class:`int`

    .. py:attribute:: ramAddress

        The address where this overlay will be placed in memory when loaded.

        :type: :py:class:`int`

    .. py:attribute:: ramSize

        The total size of the overlay once it is loaded into memory. This
        should be equal to ``len(overlay.data)`` if the overlay is
        uncompressed, or smaller than that if it is compressed.

        :type: :py:class:`int`

    .. py:attribute:: staticInitStart

        The address of the beginning of the static initializers function
        pointers table for this overlay. I think this is a table of function
        pointers that (at the C++ level) set static variables in overlay scope
        to their initial values, which are all run upon loading the overlay;
        however, I am not sure of this.

        :type: :py:class:`int`

    .. py:attribute:: staticInitEnd

        The address of the end of the static initializers function pointers
        table for this overlay. See the :py:attr:`staticInitStart` attribute
        for more information.

        :type: :py:class:`int`

    .. py:attribute:: verifyHash

        Alias property for ":py:attr:`flags` & 2". This is ``True`` if the
        overlay-loading code should calculate the overlay's HMAC and compare it
        to a (hardcoded) expected hash value, ``False`` otherwise.

        :type: :py:class:`bool`

    .. py:function:: save(*[, compress])

        Generate a :py:class:`bytes` object representing this overlay.

        Note: this function updates several attributes to match the requested
        output representation. (For example, :py:attr:`compressed` will be set
        to match the value of the ``compress`` parameter.)

        :param bool compress: Whether to compress the overlay or not.

            :default: ``False``

        :returns: The overlay file data.
        :rtype: :py:class:`bytes`


.. py:function:: loadOverlayTable(tableData, fileCallback[, idsToLoad])

    Parse ARM7 or ARM9 overlay table data to create a dictionary of
    :py:class:`Overlay`\s. This is the inverse of :py:func:`saveOverlayTable`.

    :param bytes tableData: The overlay table data.

    :param fileCallback: A function that takes an overlay ID and a file ID and
        returns the data for the requested file. This allows you to load
        overlay data by either of these IDs, whichever suits your needs best.
    :type fileCallback: function with the signature
            ``(overlayID: int, fileID: int) -> bytes``

    :param idsToLoad: A specific set of overlay IDs to load. You can use this
        to avoid loading overlays you don't actually care about, in order to
        improve your application's performance.
    :type idsToLoad: :py:class:`set` of :py:class:`int`

    :returns: A :py:class:`dict` of overlays.
    :rtype: :py:class:`dict`: ``{overlayID: overlay}`` (where ``overlayID`` is
        of type :py:class:`int` and ``overlay`` is of type :py:class:`Overlay`)


.. py:function:: saveOverlayTable(table)

    Generate a bytes object representing this dictionary of
    :py:class:`Overlay`\s, in proper ARM7 or ARM9 overlay table format. This is
    the inverse of :py:func:`loadOverlayTable`.

    :param table: A :py:class:`dict` of overlays.
    :type table: :py:class:`dict`: ``{overlayID: overlay}``, where
        ``overlayID`` is of type :py:class:`int` and ``overlay`` is of type
        :py:class:`Overlay`

    :returns: The overlay table data.
    :rtype: :py:class:`bytes`
