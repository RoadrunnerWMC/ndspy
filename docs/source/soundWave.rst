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

``ndspy.soundWave``: Sound Waves
================================

.. module:: ndspy.soundWave

The ``ndspy.soundWave`` module lets you edit and create *SWAV* streamed audio
files. These are intended to be used for instrument samples, sound effects, and
other short sounds.

A *SWAV* is conceptually similar to a standard *WAV* audio file. They define a
waveform rather than sequence events. *SWAV*\s are limited to only one channel,
and shorter loop periods than *STRM* files.

.. seealso::

    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.


.. py:class:: SWAV([file])

    An *SWAV* streamed audio file.

    :param bytes file: The data to be read as an *SWAV* file. If this is not
        provided, the *SWAV* object will initially be empty.

    .. py:attribute:: data

        The raw waveform data. This must be interpreted according to the value
        of :py:attr:`waveType`.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: isLooped

        Whether the *SWAV* is looped or just plays through once.

        .. seealso::

            You can use :py:attr:`loopOffset` to control the beginning of the
            looped region.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: loopOffset

        The beginning of the looped portion of the *SWAV* data, measured in
        words (groups of 4 bytes).

        .. warning::

            Due to how :py:attr:`totalLength` is encoded in the file data, this
            attribute *must not* be greater than it, or else you will
            experience errors upon saving (:py:func:`save`)!

        .. seealso::

            In order to loop an *SWAV*, you also need to set
            :py:attr:`isLooped` to ``True``.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: sampleRate

        The sample rate the *SWAV* should be played at.

        :type: :py:class:`int`

        :default: 8000

    .. py:attribute:: time

        A value of unclear meaning. This is pretty much always set to the
        following:

        .. code-block:: python

            strm.time = int(16756991 / strm.sampleRate)

        .. note::

            This can optionally be recalculated for you automatically upon
            saving the *SWAV*. For more information about this, see the
            documentation for the :py:func:`save` function.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: totalLength

        The total length of the *SWAV* data, measured in words (groups of 4
        bytes). This is almost always equal to ``len(swav.data) // 4``, but,
        for reasons unknown, not always.

        .. warning::

            Due to how this is encoded in the file data, this attribute *must
            not* be less than :py:attr:`loopOffset`, or else you will
            experience errors upon saving (:py:func:`save`)!

        .. note::

            This can optionally be recalculated for you automatically upon
            saving the *SWAV*. For more information about this, see the
            documentation for the :py:func:`save` function.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: waveType

        The format that this *SWAV*'s waveform data (:py:attr:`data`) is in.

        :type: :py:class:`ndspy.WaveType` (or :py:class:`int`)

        :default: :py:data:`ndspy.WaveType.PCM8`

    .. py:classmethod:: fromData([data], *[, waveType[, isLooped[, sampleRate[, time[, loopOffset[, totalLength]]]]]])

        Create an *SWAV* from raw waveform data.

        :param data: The initial value for the :py:attr:`data` attribute.

        :param waveType: The initial value for the :py:attr:`waveType`
            attribute.

        :param isLooped: The initial value for the :py:attr:`isLooped`
            attribute.

        :param sampleRate: The initial value for the :py:attr:`sampleRate`
            attribute.

        :param time: The initial value for the :py:attr:`time` attribute.

        :param loopOffset: The initial value for the :py:attr:`loopOffset`
            attribute.

        :param totalLength: The initial value for the :py:attr:`totalLength`
            attribute.

        :returns: The *SWAV* object.
        :rtype: :py:class:`SWAV`

    .. py:classmethod:: fromFile(filePath)

        Load an *SWAV* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *SWAV* file to open.
        :type filePath: :py:class:`str` or other path-like object

        :returns: The *SWAV* object.
        :rtype: :py:class:`SWAV`

    .. py:function:: save(*[, updateTime=False[, updateTotalLength=False]])

        Generate file data representing this *SWAV*.

        :param bool updateTime: If this is ``True``, :py:attr:`time` will be
            updated based on the sample rate, using the formula found in the
            documentation for the :py:attr:`time` attribute.

            :default: ``False``

        :param bool updateTotalLength: If this is ``True``,
            :py:attr:`totalLength` will be updated to be one-fourth the length
            of :py:attr:`data`.

            :default: ``False``

        :returns: The *SWAV* file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath, *[, updateTime=False[, updateTotalLength=False]])

        Generate file data representing this *SAV*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *SAV* file to save to.
        :type filePath: :py:class:`str` or other path-like object

        :param bool updateTime: If this is ``True``, :py:attr:`time` will be
            updated based on the sample rate, using the formula found in the
            documentation for the :py:attr:`time` attribute.

            :default: ``False``

        :param bool updateTotalLength: If this is ``True``,
            :py:attr:`totalLength` will be updated to be one-fourth the length
            of :py:attr:`data`.

            :default: ``False``
