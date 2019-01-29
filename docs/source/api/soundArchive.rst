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

``ndspy.soundArchive``: SDAT (Sound Archives)
=============================================

.. module:: ndspy.soundArchive

``ndspy.soundArchive`` allows you to load and save *SDAT* sound archive files
and the files within them.

.. seealso::
    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <../appendices/sdat-structure>`.

.. py:class:: SDAT([data])

    A sound data archive file (*SDAT*).

    :param bytes data: The data to be read as an *SDAT* file. If not provided,
        the *SDAT* will use default values.

    .. py:attribute:: banks

        The instrument banks in this *SDAT*, in the form of a list of
        name-value pairs containing :py:class:`ndspy.soundBank.SBNK` instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, bank)``, where ``name`` is of type
            :py:class:`str` and ``bank`` is of type
            :py:class:`ndspy.soundBank.SBNK` or ``None``

        :default: ``[]``

    .. py:attribute:: groups

        The file groups in this *SDAT*, in the form of a list of name-value
        pairs, where the values are lists containing
        :py:class:`ndspy.soundGroup.GroupEntry` instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, entries)``, where ``name`` is of
            type :py:class:`str` and ``entries`` is ``None`` or a list of
            :py:class:`ndspy.soundGroup.GroupEntry`\s

        :default: ``[]``

    .. py:attribute:: sequenceArchives

        The sound-effect sequence archives in this *SDAT*, in the form of a
        list of name-value pairs containing
        :py:class:`ndspy.soundSequenceArchive.SSAR` instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can
            use to find and replace values in this list.

        :type: :py:class:`list` of ``(name, sequenceArchive)``, where ``name``
            is of type :py:class:`str` and ``sequenceArchive`` is of type
            :py:class:`ndspy.soundSequenceArchive.SSAR` or ``None``

        :default: ``[]``

    .. py:attribute:: sequencePlayers

        The sequence players in this *SDAT*, in the form of a list of
        name-value pairs containing
        :py:class:`ndspy.soundSequencePlayer.SequencePlayer` instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, sequencePlayer)``, where ``name``
            is of type :py:class:`str` and ``sequencePlayer`` is of type
            :py:class:`ndspy.soundSequencePlayer.SequencePlayer` or ``None``

        :default: ``[]``

    .. py:attribute:: sequences

        The sequenced music pieces in this *SDAT*, in the form of a list of
        name-value pairs containing :py:class:`ndspy.soundSequence.SSEQ`
        instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, sequence)``, where ``name`` is of
            type :py:class:`str` and ``sequence`` is of type
            :py:class:`ndspy.soundSequence.SSEQ` or ``None``

        :default: ``[]``

    .. py:attribute:: streamPlayers

        The stream players in this *SDAT*, in the form of a list of name-value
        pairs containing :py:class:`ndspy.soundStreamPlayer.StreamPlayer`
        instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, streamPlayer)``, where ``name`` is
            of type :py:class:`str` and ``streamPlayer`` is of type
            :py:class:`ndspy.soundStreamPlayer.StreamPlayer` or ``None``

        :default: ``[]``

    .. py:attribute:: streams

        The streamed music pieces in this *SDAT*, in the form of a list of
        name-value pairs containing :py:class:`ndspy.soundStream.STRM`
        instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, stream)``, where ``name`` is of
            type :py:class:`str` and ``stream`` is of type
            :py:class:`ndspy.soundStream.STRM` or ``None``

        :default: ``[]``

    .. py:attribute:: waveArchives

        The archive files containing wave files in this *SDAT*, in the form of
        a list of name-value pairs containing
        :py:class:`ndspy.soundWaveArchive.SWAR` instances.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, waveArchive)``, where ``name`` is
            of type :py:class:`str` and ``waveArchive`` is of type
            :py:class:`ndspy.soundWaveArchive.SWAR` or ``None``

        :default: ``[]``

    .. py:attribute:: fatLengthsIncludePadding

        If this is ``True``, files within this *SDAT* will be extended with
        null bytes to provide the proper alignment. If this is ``False``, null
        bytes for alignment will still be present, but they will be between
        files rather than appended to the previous file.

        This is chosen heuristically when loading an *SDAT*, so it may not
        always be accurate. If this value matters to you, it's a good idea to
        explicitly set it to the value you want before saving.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: fileAlignment

        The alignment of files within this *SDAT*. Null bytes will be placed
        between files in order to ensure that all files begin at an offset in
        the ROM data that is a multiple of this value.

        This is chosen heuristically when loading an *SDAT*, so it may not
        always be accurate. If this value matters to you, it's a good idea to
        explicitly set it to the value you want before saving.

        .. seealso::

            :py:attr:`firstFileAlignment` -- the alignment of the first file,
            which may differ from this value.

            :py:attr:`fatLengthsIncludePadding` -- whether the padding used to
            align files should be included in the file lengths or not.

        :type: :py:class:`int`

        :default: 0x20

    .. py:attribute:: firstFileAlignment

        The alignment of the first file within this *SDAT*. If this is
        ``None``, the alignment will be the same as for other files.

        This is chosen heuristically when loading an *SDAT*, so it may not
        always be accurate. If this value matters to you, it's a good idea to
        explicitly set it to the value you want before saving.

        .. seealso::

            :py:attr:`fileAlignment` -- the alignment of all other files.

        :type: :py:class:`int` or ``None``

        :default: ``None``

    .. py:attribute:: padAtEnd

        If this is ``True``, alignment padding will be added at the very end of
        the *SDAT* (after the last file) or not. This is fairly pointless, but
        most *SDAT* files do this. Only *SDAT* files from modified games seem
        to not do this.

        This is chosen heuristically when loading an *SDAT*, so it may not
        always be accurate. If this value matters to you, it's a good idea to
        explicitly set it to the value you want before saving.

        .. seealso::

            :py:attr:`fatLengthsIncludePadding` -- whether the padding used to
            align files should be included in the file lengths or not.

        :type: :py:class:`bool`

        :default: ``True``

    .. py:attribute:: padSymbSizeTo4InSDATHeader

        If this is ``True``, the alignment padding at the end of the "SYMB"
        block will be included in its length. Only *SDAT* files from modified
        games seem to do this.

        This is chosen heuristically when loading an *SDAT*, so it may not
        always be accurate. If this value matters to you, it's a good idea to
        explicitly set it to the value you want before saving.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:classmethod:: fromFile(filePath)

        Load an *SDAT* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *SDAT* file to open.
        :type filePath: :py:class:`str` or other path-like object

        :returns: The *SDAT* object.
        :rtype: :py:class:`SDAT`

    .. py:function:: save()

        Generate file data representing this *SDAT*.

        :returns: The *SDAT* file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *SDAT*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *SDAT* file to save to.
        :type filePath: :py:class:`str` or other path-like object
