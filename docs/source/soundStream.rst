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

``ndspy.soundStream``: Sound Streams
====================================

.. module:: ndspy.soundStream

The ``ndspy.soundStream`` module lets you edit and create *STRM* streamed audio
files. These are intended to be used for background music.

A *STRM* is conceptually similar to a standard *WAV* audio file. They define a
waveform rather than sequence events. They support multiple channels, and
longer loops than *SWAV*\s do. These are less commonly used than *SSEQ*
sequenced audio files due to their much larger file size.

.. warning::

    All *STRM*\s I've found in retail games which have multiple blocks per
    channel use the ADPCM wave type (:py:attr:`waveType` ``=``
    :py:data:`ndspy.WaveType.ADPCM`). This may be due to a hardware limitation
    explained `on GBATEK <https://problemkaputt.de/gbatek.htm#dssoundnotes>`_
    (see the section about the "Hold Flag (appears useless/bugged)"). You may
    run into issues playing *STRM*\s with multiple blocks per channel and some
    other wave data format.

.. seealso::

    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.


.. py:class:: STRM([file[, unk02[, volume[, priority[, playerID[, unk07]]]]]])

    A *STRM* streamed audio file. This is a piece of music, usually used for
    background music or jingles.

    :param bytes file: The data to be read as an *STRM* file. If this is not
        provided, the *STRM* object will initially be empty.

    :param unk02: The initial value for the :py:attr:`unk02` attribute.

    :param volume: The initial value for the :py:attr:`volume` attribute.

    :param priority: The initial value for the :py:attr:`priority` attribute.

    :param playerID: The initial value for the :py:attr:`playerID` attribute.

    :param unk07: The initial value for the :py:attr:`unk07` attribute.

    .. py:attribute:: channels

        This attribute contains the *STRM*'s raw waveform data, organized by
        channel and block.

        This attribute is a list where each element represents a channel. Each
        of these channels is itself a list of :py:class:`bytes` objects
        representing blocks of wave data. Many *STRM*\s have channels that are
        only one block long, but some have hundreds or even thousands of
        blocks per channel.

        .. warning::

            There are some restrictions on what you're allowed to put in here,
            and you'll experience errors upon trying to save (:py:func:`save`)
            if you don't follow them:

            *   All channels must have the same number of blocks:

                .. code-block:: python

                    for c in strm.channels:
                        assert len(c) == len(strm.channels[0])

            *   All of the blocks in a given channel must be of the same size,
                except for the last block, which can be a different size from
                the others (typically shorter, but this isn't enforced):

                .. code-block:: python

                    for c in strm.channels:
                        for b in c[:-1]:
                            assert len(b) == len(c[0])

            *   The lengths of the blocks in all channels must match:

                .. code-block:: python

                    for c in strm.channels:
                        for i, b in enumerate(c):
                            assert len(b) == len(strm.channels[0][i])

        .. note::

            If the :py:attr:`waveType` is :py:data:`ndspy.WaveType.ADPCM`,
            every block must begin with its own ADPCM header. More information
            about ADPCM headers can be found on `GBATEK
            <https://problemkaputt.de/gbatek.htm#dssoundnotes>`_.

        :type: :py:class:`list` of :py:class:`list` of :py:class:`bytes`

        :default: ``[]``

    .. py:attribute:: dataMergeOptimizationID

        When saving a *SDAT* file containing multiple *STRM* files, ndspy will
        check if any of them save to identical data. If it finds any, it will
        only encode the data for them once and then reference it multiple
        times, to save some space. This attribute is an extra field that is
        also compared between *STRM* files, which you can use to exclude
        particular ones from this optimization.

        Since this defaults to 0 for all *STRM*\s created from scratch, this
        optimization will happen by default. It's unlikely that you will need
        to use this attribute to disable the optimization, but you can.

        .. note::

            This value is not explicitly saved in the *STRM* file or in the
            *SDAT* file containing it.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: isLooped

        Whether the *STRM* is looped or just plays through once.

        .. seealso::

            You can use :py:attr:`loopOffset` to control the beginning of the
            looped region.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: loopOffset

        The beginning of the looped portion of the *STRM* data, measured in
        samples.

        .. seealso::

            In order to loop a *STRM*, you also need to set :py:attr:`isLooped`
            to ``True``.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: playerID

        The ID of the stream player that will be used to play this stream.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: priority

        The stream's "priority." The exact meaning of this is unclear.

        :type: :py:class:`int`

        :default: 64

    .. py:attribute:: sampleRate

        The sample rate the *STRM* should be played at.

        :type: :py:class:`int`

        :default: 8000

    .. py:attribute:: samplesInLastBlock

        The length in samples of each channel's last block of waveform data
        (:py:attr:`channels`).

        .. seealso::

            :py:attr:`samplesPerBlock` -- the corresponding attribute that
            defines the number of samples in all blocks except for each
            channel's last one.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: samplesPerBlock

        The length in samples of each individual block of waveform data (in
        :py:attr:`channels`), per channel, ignoring the final block of each
        channel.

        .. seealso::

            :py:attr:`samplesInLastBlock` -- the corresponding attribute that
            defines the number of samples in each channel's last block.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: time

        A value of unclear meaning. This is pretty much always set to the
        following:

        .. code-block:: python

            strm.time = int(1.0 / strm.sampleRate * 16756991 / 32)

        .. note::

            This can optionally be recalculated for you automatically upon
            saving the *STRM*. For more information about this, see the
            documentation for the :py:func:`save` function.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk02

        The value following the *STRM*'s file ID in the "INFO" section of the
        *SDAT* file it is contained in. Its purpose is unknown.

        .. note::

            This value is not explicitly saved in the *STRM* file, but it is
            saved in the *SDAT* file if the *STRM* is within one.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk07

        The value following the *STRM*'s player ID in the "INFO" section of the
        *SDAT* file it is contained in. Its purpose is unknown.

        .. note::

            This value is not explicitly saved in the *STRM* file, but it is
            saved in the *SDAT* file if the *STRM* is within one.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk03

        A value of unknown purpose at offset 0x1B (relative to the beginning
        of the file) in the *STRM* file header.

        Based on its location relative to surrounding values, this could be a
        meaningless padding byte for alignment.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk28

        A value of unknown purpose at offset 0x40 (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk2C

        A value of unknown purpose at offset 0x44 (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk30

        A value of unknown purpose at offset 0x48 (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk34

        A value of unknown purpose at offset 0x4C (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk38

        A value of unknown purpose at offset 0x50 (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk3C

        A value of unknown purpose at offset 0x54 (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk40

        A value of unknown purpose at offset 0x58 (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk44

        A value of unknown purpose at offset 0x5C (relative to the beginning
        of the file) in the *STRM* file header.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: volume

        The overall volume of the stream. This is an integer between 0 and
        127, inclusive. You should usually leave this as 127.

        :type: :py:class:`int`

        :default: 127

    .. py:attribute:: waveType

        The format that this *STRM*'s waveform data (:py:attr:`channels`) is
        in.

        :type: :py:class:`ndspy.WaveType` (or :py:class:`int`)

        :default: :py:data:`ndspy.WaveType.PCM8`

    .. py:classmethod:: fromChannels(channels[, unk02[, volume[, priority[, playerID[, unk07]]]]])

        Create a *STRM* from a list of channels.

        :param channels: The initial value for the :py:attr:`channels`
            attribute.

        :param unk02: The initial value for the :py:attr:`unk02` attribute.

        :param volume: The initial value for the :py:attr:`volume` attribute.

        :param priority: The initial value for the :py:attr:`priority`
            attribute.

        :param playerID: The initial value for the :py:attr:`playerID`
            attribute.

        :param unk07: The initial value for the :py:attr:`unk07` attribute.

        :returns: The *STRM* object.
        :rtype: :py:class:`STRM`

    .. py:classmethod:: fromFile(filePath[, ...])

        Load a *STRM* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *STRM* file to open.
        :type filePath: :py:class:`str` or other path-like object

        Further parameters are the same as those of the default constructor.

        :returns: The *STRM* object.
        :rtype: :py:class:`STRM`

    .. py:function:: save(*[, updateTime=False])

        Generate file data representing this *STRM*, and then return that data,
        :py:attr:`unk02`, :py:attr:`volume`, :py:attr:`priority`,
        :py:attr:`playerID`, and :py:attr:`unk07`, as a 6-tuple. This matches
        the parameters of the default class constructor.

        :param bool updateTime: If this is ``True``, :py:attr:`time` will be
            updated based on the sample rate, using the formula found in the
            documentation for the :py:attr:`time` attribute.

            :default: ``False``

        :returns: The *STRM* file data, :py:attr:`unk02`, :py:attr:`volume`,
            :py:attr:`priority`, :py:attr:`playerID`, and :py:attr:`unk07`.

        :rtype: ``(data, unk02, volume, priority, playerID, unk07)``, where
            ``data`` is of type :py:class:`bytes` and all of the other elements
            are of type :py:class:`int`

    .. py:function:: saveToFile(filePath, *[, updateTime=False])

        Generate file data representing this *STRM*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *STRM* file to save to.
        :type filePath: :py:class:`str` or other path-like object

        :param bool updateTime: If this is ``True``, :py:attr:`time` will be
            updated based on the sample rate, using the formula found in the
            documentation for the :py:attr:`time` attribute.

            :default: ``False``
