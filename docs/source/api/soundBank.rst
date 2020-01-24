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

``ndspy.soundBank``: Instrument Banks
=====================================

.. module:: ndspy.soundBank

The ``ndspy.soundBank`` module contains classes and functions related to the
*SBNK* instrument bank file included in *SDAT* sound archives.

.. seealso::
    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <../appendices/sdat-structure>`.


.. data:: NO_INSTRUMENT_TYPE

    The type value of a nonexistent instrument: 0.

.. data:: SINGLE_NOTE_PCM_INSTRUMENT_TYPE

    The type value of a :py:class:`SingleNoteInstrument` that plays a
    *SWAV* from a *SWAR*: 1.

.. data:: SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE

    The type value of a :py:class:`SingleNoteInstrument` that plays a
    square wave using the Nintendo DS's PSG hardware: 2.

.. data:: SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE

    The type value of a :py:class:`SingleNoteInstrument` that plays
    white noise using the Nintendo DS's PSG hardware: 3.

.. data:: RANGE_INSTRUMENT_TYPE

    The type value of a :py:class:`RangeInstrument`: 16.

.. data:: REGIONAL_INSTRUMENT_TYPE

    The type value of a :py:class:`RegionalInstrument`: 17.


.. py:class:: NoteType

    :base class: :py:class:`enum.IntEnum`

    An enumeration that distinguishes between the three primary types of note
    definitions.

    .. seealso::

        :py:class:`NoteDefinition` -- for more information about these type
        values.

    .. data:: PCM

        The type value of a :py:class:`NoteDefinition` that plays an *SWAV*
        from a *SWAR*: 1.

    .. data:: PSG_SQUARE_WAVE

        The type value of a :py:class:`NoteDefinition` that plays a square wave
        using the Nintendo DS's PSG hardware: 2.

    .. data:: PSG_WHITE_NOISE

        The type value of a :py:class:`NoteDefinition` that plays white noise
        using the Nintendo DS's PSG hardware: 3.


.. py:class:: NoteDefinition([waveID_dutyCycle[, waveArchiveIDID[, pitch[, attack[, decay[, sustain[, release[, pan[, type]]]]]]]]])

    A note definition within a *SBNK* instrument. This can be thought of as a
    template from which many notes of different pitches can be played.

    There are three known meaningful type values (:py:attr:`type`) associated
    with this class, which affect which attributes are meaningful:

    *   :py:data:`NoteType.PCM` will produce a PCM note definition, which can
        play a *SWAV* wave file from a *SWAR* wave archive file.

        If the note definition is of this type, you can use the
        :py:attr:`waveID` and :py:attr:`waveArchiveIDID` attributes to set the
        *SWAV* and *SWAR* IDs, respectively.

    *   :py:data:`NoteType.PSG_SQUARE_WAVE` will produce a PSG square-wave note
        definition, which uses the Nintendo DS's PSG hardware to play a square
        wave.

        If the instrument is of this type, you can use the :py:attr:`dutyCycle`
        attribute to set the square wave's duty cycle.

    *   :py:data:`NoteType.PSG_WHITE_NOISE` will produce a PSG white noise note
        definition, which uses the Nintendo DS's PSG hardware to play white
        noise.

        There are no attributes that are specific to this instrument type.

    Attributes not mentioned above will work with all type values.

    :param waveID_dutyCycle: The initial value for the :py:attr:`waveID` and
        :py:attr:`dutyCycle` attributes.

    :param waveArchiveIDID: The initial value for the :py:attr:`waveArchiveIDID`
        attribute.

    :param pitch: The initial value for the :py:attr:`pitch` attribute.

    :param attack: The initial value for the :py:attr:`attack` attribute.

    :param decay: The initial value for the :py:attr:`decay` attribute.

    :param sustain: The initial value for the :py:attr:`sustain` attribute.

    :param release: The initial value for the :py:attr:`release` attribute.

    :param pan: The initial value for the :py:attr:`pan` attribute.

    :param type: The initial value for the :py:attr:`type` attribute.

    .. py:attribute:: attack

        The speed at which the note will fade from 0 to 100% volume when it
        begins to play. 0 is the slowest speed possible, and 127 is instant.

        .. seealso::

            `The Wikipedia page on envelope
            <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
            decay, sustain, and release values.

            Section 4.2 (Articulation Data) in the `kiwi.ds Nitro Composer File
            (*.sdat) Specification
            <https://sites.google.com/site/kiwids/sdat.html>`_ explains this in
            more detail.

            .. note::

                The link in the sentence "See this file for more details on how
                to interpret the articulation data" may be broken; `here is the
                correct link
                <https://sites.google.com/site/kiwids/articulation.htm>`__.

        :type: :py:class:`int`

        :default: 127

    .. py:attribute:: decay

        The speed at which the note will fade from 100% volume to the
        :py:attr:`sustain` level after the :py:attr:`attack` phase is finished.
        0 is the slowest speed possible, and 127 is instant.

        .. seealso::

            `The Wikipedia page on envelope
            <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
            decay, sustain, and release values.

            Section 4.2 (Articulation Data) in the `kiwi.ds Nitro Composer File
            (*.sdat) Specification
            <https://sites.google.com/site/kiwids/sdat.html>`_ explains this in
            more detail.

            .. note::

                The link in the sentence "See this file for more details on how
                to interpret the articulation data" may be broken; `here is the
                correct link
                <https://sites.google.com/site/kiwids/articulation.htm>`__.

        :type: :py:class:`int`

        :default: 127

    .. py:attribute:: dutyCycle

        The `duty cycle <https://en.wikipedia.org/wiki/Duty_cycle>`_ of the PSG
        square wave defined by this note definition. Values are as follows:

        ===============  =================
        Attribute value  Actual duty cycle
        ===============  =================
               0               12.5%
               1               25%
               2               37.5%
               3               50%
               4               62.5%
               5               75%
               6               87.5%
               7               0%
        ===============  =================

        Higher values are bitwise-AND-ed with 7.

        .. note::

            This only has an effect if :py:attr:`type` is
            :py:data:`NoteType.PSG_SQUARE_WAVE`.

        .. note::

            This is an alias for :py:attr:`waveID`. This does not cause
            conflicts, since this attribute only affects note definitions that
            define PSG square waves, which do not use *SWAV*\s at all.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: pan

        The note's `stereo panning value
        <https://en.wikipedia.org/wiki/Panning_%28audio%29>`_. A value of 64 is
        centered. Smaller values pan to the left, and larger values pan to the
        right.

        .. note::

            *SSEQ* sequence events can also specify panning values, using
            :py:class:`ndspy.soundSequence.PanSequenceEvent`\s. The interplay
            between instrument and track panning may cause your track's sounds
            to ultimately be panned differently from how your :py:attr:`pan`
            value dictates.

        :type: :py:class:`int`

        :default: 64

    .. py:attribute:: pitch

        The pitch number that the instrument sample wave plays. This is used to
        calculate the adjusted sample rate that the wave needs to be played at
        to produce a desired actual pitch in the sequence.

        This is measured in half-steps; 60 is middle C. Valid values are
        between 0 and 127, inclusive.

        :type: :py:class:`int`

        :default: 60

    .. py:attribute:: release

        The speed at which the note will fade from the :py:attr:`sustain` level
        to 0% volume when it is released. 0 is the slowest speed possible, and
        127 is instant.

        .. seealso::

            `The Wikipedia page on envelope
            <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
            decay, sustain, and release values.

            Section 4.2 (Articulation Data) in the `kiwi.ds Nitro Composer File
            (*.sdat) Specification
            <https://sites.google.com/site/kiwids/sdat.html>`_ explains this in
            more detail.

            .. note::

                The link in the sentence "See this file for more details on how
                to interpret the articulation data" may be broken; `here is the
                correct link
                <https://sites.google.com/site/kiwids/articulation.htm>`__.

        :type: :py:class:`int`

        :default: 127

    .. py:attribute:: sustain

        The volume that the note will remain at after the :py:attr:`attack` and
        :py:attr:`decay` phases are finished. 0 is no volume, and 127 is 100%
        volume.

        .. seealso::

            `The Wikipedia page on envelope
            <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
            decay, sustain, and release values.

            Section 4.2 (Articulation Data) in the `kiwi.ds Nitro Composer File
            (*.sdat) Specification
            <https://sites.google.com/site/kiwids/sdat.html>`_ explains this in
            more detail.

            .. note::

                The link in the sentence "See this file for more details on how
                to interpret the articulation data" may be broken; `here is the
                correct link
                <https://sites.google.com/site/kiwids/articulation.htm>`__.

        :type: :py:class:`int`

        :default: 127

    .. py:attribute:: type

        The type of sound that will be produced when this note definition is
        played. The value of this attribute affects whether other attributes
        are meaningful or not, such as :py:attr:`dutyCycle`, :py:attr:`waveID`,
        and :py:attr:`waveArchiveIDID`.

        .. warning::

            If this note definition is within a
            :py:class:`SingleNoteInstrument`, this attribute is an alias for
            :py:attr:`SingleNoteInstrument.type` (automatically cast to and
            from :py:class:`NoteType` for you). See the documentation for
            :py:attr:`SingleNoteInstrument.type` for more information.

        .. seealso::

            :py:class:`NoteDefinition` -- for more information about valid
            values for this attribute.

        :type: :py:class:`NoteType` (or :py:class:`int`)

        :default: :py:data:`NoteType.PCM`

    .. py:attribute:: waveArchiveIDID

        An index into the *SWAR* IDs list of the *SBNK* this note definition is
        a part of (:py:attr:`SBNK.waveArchiveIDs`). This, in turn, indicates
        the ID number (index) of the *SWAR* where the *SWAV* for this note's
        instrument sample can be found.

        .. warning::

            This is *not* the index of the *SWAR* in
            :py:attr:`ndspy.soundArchive.SDAT.waveArchives`!

            For example, if this attribute has a value 3, you would look up
            ``sbnk.waveArchiveIDs[3]`` in the *SBNK* this note definition
            resides in. The value you find there is the actual *SWAR* ID, which
            you can use to get the actual *SWAR* from the *SDAT*:
            ``sdat.waveArchives[swarID]``.

        .. note::

            This only has an effect if :py:attr:`type` is
            :py:data:`NoteType.PCM`.

        .. seealso::
            :py:attr:`waveID` -- the ID number of the *SWAV* to use from the
            *SWAR*.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: waveID

        The ID number (index) of the *SWAV* to use as the instrument sample for
        this note.

        .. note::

            This only has an effect if :py:attr:`type` is
            :py:data:`NoteType.PCM`.

        .. note::

            This is an alias for :py:attr:`dutyCycle`. This does not cause
            conflicts, since that attribute only affects note definitions that
            define PSG square waves, which do not use *SWAV*\s at all.

        .. seealso::
            :py:attr:`waveArchiveIDID` -- the ID number of the ID number of the
            *SWAR* where this *SWAV* can be found.

        :type: :py:class:`int`

        :default: 0

    .. py:classmethod:: fromData(data[, type])

        Create a note definition from raw file data that does not include the
        :py:attr:`type` value at the beginning.

        .. seealso::
            :py:func:`fromDataWithType` -- use this function instead if the
            file data does include :py:attr:`type`.

        :param bytes data: The data to be read. Only the first 10 bytes will be
            used.

        :param type: The initial value for the :py:attr:`type` attribute.

        :returns: The note definition object.
        :rtype: :py:class:`NoteDefinition`

    .. py:classmethod:: fromDataWithType(data)

        Create a note definition from raw file data that includes the
        :py:attr:`type` value at the beginning.

        .. seealso::
            :py:func:`fromData` -- use this function instead if the file data
            does not include :py:attr:`type`.

        :param bytes data: The data to be read. Only the first 12 bytes will be
            used.

        :returns: The note definition object.
        :rtype: :py:class:`NoteDefinition`

    .. py:function:: save()

        Generate data representing this note definition, without including the
        :py:attr:`type` value at the beginning.

        .. seealso::
            :py:func:`saveWithType` -- use this function instead if you want
            the data to include :py:attr:`type`.

        :returns: The note definition data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveWithType()

        Generate data representing this note definition, including the
        :py:attr:`type` value at the beginning.

        .. seealso::
            :py:func:`save` -- use this function instead if you do not want the
            data to include :py:attr:`type`.

        :returns: The note definition data.
        :rtype: :py:class:`bytes`


.. py:class:: Instrument(type)

    An instrument within a *SBNK* file.

    This is an abstract base class, and should be subclassed in order to be
    used.

    .. seealso::

        :py:class:`SingleNoteInstrument` -- the subclass that should be used
        for :py:attr:`type` values 1 through 15
        (:py:const:`SINGLE_NOTE_PCM_INSTRUMENT_TYPE`,
        :py:const:`SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE`, and
        :py:const:`SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE`).

        :py:class:`RangeInstrument` -- the subclass that should be used for
        :py:attr:`type` value 16
        (:py:const:`RANGE_INSTRUMENT_TYPE`).

        :py:class:`RegionalInstrument` -- the subclass that should be used for
        :py:attr:`type` value 17
        (:py:const:`REGIONAL_INSTRUMENT_TYPE`).

    :param type: The initial value for the :py:attr:`type` attribute.

    .. py:attribute:: bankOrderKey

        This attribute has to do with the way instrument data structs are
        sorted within the *SBNK*. The data structs are always first sorted by
        instrument type (first types < 16, then type 16, then type 17). Within
        each of those three groups, though, the order is arbitrary. Thus, this
        key allows you to set up whatever arrangement you want.
        
        It's extremely unlikely that you'll ever need to look at or change
        this, since the order of the structs doesn't really affect anything.

        .. note::

            This value is not explicitly saved in the *SBNK* file.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: dataMergeOptimizationID

        When saving a *SBNK*, ndspy will check if any instruments have
        identical data. If it finds any, it will only encode the data for them
        once and then reference it multiple times, to save some space. This
        attribute is an extra field that is also compared between instruments,
        which you can use to exclude particular instruments from this
        optimization.

        Since this defaults to 0 for all instruments created from scratch, this
        optimization will happen by default. It's unlikely that you will need
        to use this attribute to disable the optimization, but you can.

        .. note::

            This value is not explicitly saved in the *SBNK* file.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: type

        The type value of this instrument.

        .. warning::

            In the :py:class:`SingleNoteInstrument` subclass, this is an alias
            for ``instrument.noteDefinition.type``. See
            :py:attr:`SingleNoteInstrument.type` for more information.

        .. seealso::

            :py:const:`NO_INSTRUMENT_TYPE`,
            :py:const:`SINGLE_NOTE_PCM_INSTRUMENT_TYPE`,
            :py:const:`SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE`,
            :py:const:`SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE`,
            :py:const:`RANGE_INSTRUMENT_TYPE`,
            :py:const:`REGIONAL_INSTRUMENT_TYPE` -- type values for known
            instrument types.

        :type: :py:class:`int`

    .. py:classmethod:: fromData(type, data, startOffset)

        Create an instrument from raw file data.

        This method must be implemented in subclasses; this abstract-base-class
        implementation simply raises :py:exc:`NotImplementedError`.

        :param type: The initial value for the :py:attr:`type` attribute.

        :param bytes data: The data to be read. The instrument data need not be
            at the beginning of it.

        :param int startOffset: The offset in the data where the instrument
            data begins. This is not the place in the *SBNK* where the
            instrument type value is; rather, it is the place pointed to by the
            offset that comes just after that.

        :returns: The instrument object, and the number of bytes that were read
            to create it.

        :rtype: ``(instrument, bytesRead)``, where ``instrument`` is of type
            :py:class:`Instrument` and ``bytesRead`` is of type
            :py:class:`int`.

    .. py:function:: save()

        Return the instrument's type value as a 1-tuple. Subclasses may return
        longer tuples with more data; currently, all subclasses add a
        :py:class:`bytes` instance.

        :returns: The instrument's type value as a 1-tuple.

        :rtype: ``(type,)``, where ``type`` is of type :py:class:`int`


.. py:class:: SingleNoteInstrument(noteDefinition)

    :base class: :py:class:`Instrument`

    An instrument that contains one note definition and nothing else. This is
    usually used for sound effects, which often contain one sound each anyway.
    This class encompasses instrument type (:py:attr:`Instrument.type`) values
    1 through 15.

    See the base class documentation (:py:class:`Instrument`) for information
    about inherited functions and attributes.

    :param noteDefinition: The initial value for the :py:attr:`noteDefinition`
        attribute.

    .. py:attribute:: noteDefinition

        The note definition that this instrument will use.

        :type: :py:class:`NoteDefinition`

    .. py:attribute:: type

        The type value of this instrument. See :py:attr:`Instrument.Type` for
        more information.

        .. warning::

            The type values for a single-note instrument and its note
            definition are encoded as a single shared value in the *SBNK* file;
            thus, they are required to be the same. As such, this property is
            an alias for ``instrument.noteDefinition.type`` (automatically cast
            to and from :py:class:`int` for you).

            .. seealso::

                :py:attr:`NoteDefinition.type` -- the attribute that this is an
                alias of.

        :type: :py:class:`int`

    .. py:classmethod:: fromData(type, data, startOffset)

        Create a single-note instrument from raw file data.

        :param type: The initial value for the :py:attr:`type` attribute. This
            should be between 1 and 15, inclusive.

        :param bytes data: The data to be read. The instrument data need not be
            at the beginning of it.

        :param int startOffset: The offset in the data where the instrument
            data begins. This is not the place in the *SBNK* where the
            instrument type value is; rather, it is the place pointed to by the
            offset that comes just after that.

        :returns: The instrument object, and the number of bytes that were read
            to create it.

        :rtype: ``(instrument, bytesRead)``, where ``instrument`` is of type
            :py:class:`SingleNoteInstrument` and ``bytesRead`` is of type
            :py:class:`int`.

    .. py:function:: save()

        Generate file data representing this instrument, and then return the
        instrument's type value and that data as a pair.

        :returns: The instrument's type value and data representing the
            instrument, as a pair.

        :rtype: ``(type, data)``, where ``type`` is of type :py:class:`int` and
            ``data`` is of type :py:class:`bytes`


.. py:class:: RangeInstrument(firstPitch, noteDefinitions)

    :base class: :py:class:`Instrument`

    An instrument that contains one note definition for each pitch in a given
    range. This is usually used for drumsets, since it is ideal for instruments
    with many distinct sounds that each only need to be played at one pitch.
    This class is for instrument type (:py:attr:`Instrument.type`) value 16
    (:py:const:`RANGE_INSTRUMENT_TYPE`).

    See the base class documentation (:py:class:`Instrument`) for information
    about inherited functions and attributes.

    :param firstPitch: The initial value for the :py:attr:`firstPitch`
        attribute.

    :param noteDefinitions: The initial value for the
        :py:attr:`noteDefinitions` attribute.

    .. py:attribute:: firstPitch

        The pitch number that can be played to access the first note in
        :py:attr:`noteDefinitions`. The second note (if there is one) can then
        be played as this value plus 1, and so on.

        This is measured in half-steps; 60 is middle C. Valid values are
        between 0 and 127, inclusive.

        :type: :py:class:`int`

    .. py:attribute:: noteDefinitions

        The list of note definitions that this instrument will use.

        :type: :py:class:`list` of :py:class:`NoteDefinition`

    .. py:classmethod:: fromData(_, data, startOffset)

        Create a range instrument from raw file data.

        :param _: Ignored. This exists as a placeholder for the "type"
            parameter that exists in the signature of this function in the
            superclass (:py:class:`Instrument`), so that this function can be
            called without any special-casing.
        :type _: any type

        :param bytes data: The data to be read. The instrument data need not be
            at the beginning of it.

        :param int startOffset: The offset in the data where the instrument
            data begins. This is not the place in the *SBNK* where the
            instrument type value is; rather, it is the place pointed to by the
            offset that comes just after that.

        :returns: The instrument object, and the number of bytes that were read
            to create it.

        :rtype: ``(instrument, bytesRead)``, where ``instrument`` is of type
            :py:class:`RangeInstrument` and ``bytesRead`` is of type
            :py:class:`int`.

    .. py:function:: save()

        Generate file data representing this instrument, and then return the
        instrument's type value and that data as a pair.

        :returns: The instrument's type value and data representing the
            instrument, as a pair.

        :rtype: ``(type, data)``, where ``type`` is of type :py:class:`int` and
            ``data`` is of type :py:class:`bytes`


.. py:class:: RegionalInstrument(regions)

    :base class: :py:class:`Instrument`

    An instrument that partitions the range [0, 127] into sections, and
    contains one note definition for each. This is used for most musical
    instruments, because it lets you use a few samples to cover a large range
    of pitches. Using a different sample for each note would be more accurate,
    but would use much more memory. Using only one sample for an instrument
    would cause it to sound increasingly distorted when playing notes that are
    far away from the sample's pitch.

    This class is for instrument type (:py:attr:`Instrument.type`) value 17
    (:py:const:`REGIONAL_INSTRUMENT_TYPE`).

    See the base class documentation (:py:class:`Instrument`) for information
    about inherited functions and attributes.

    :param regions: The initial value for the :py:attr:`regions` attribute.

    .. py:attribute:: regions

        The list of regions included in this instrument. These should be sorted
        in order of increasing :py:attr:`Region.lastPitch`, and the last region
        should have :py:attr:`Region.lastPitch` = 127. This ensures that the
        entire range of pitches from 0 to 127 inclusive is covered.

        You can define up to 8 regions. The realistic minimum number of regions
        is 1 (although such an instrument would probably be better represented
        as a :py:class:`SingleNoteInstrument`); you can save a regional
        instrument with no regions, but it is unknown how such an instrument
        would behave in an actual game.

        :type: :py:class:`list` of :py:class:`Region`

    .. py:classmethod:: fromData(_, data, startOffset)

        Create a regional instrument from raw file data.

        :param _: Ignored. This exists as a placeholder for the "type"
            parameter that exists in the signature of this function in the
            superclass (:py:class:`Instrument`), so that this function can be
            called without any special-casing.
        :type _: any type

        :param bytes data: The data to be read. The instrument data need not be
            at the beginning of it.

        :param int startOffset: The offset in the data where the instrument
            data begins. This is not the place in the *SBNK* where the
            instrument type value is; rather, it is the place pointed to by the
            offset that comes just after that.

        :returns: The instrument object, and the number of bytes that were read
            to create it.

        :rtype: ``(instrument, bytesRead)``, where ``instrument`` is of type
            :py:class:`RegionalInstrument` and ``bytesRead`` is of type
            :py:class:`int`.

    .. py:function:: save()

        Generate file data representing this instrument, and then return the
        instrument's type value and that data as a pair.

        :returns: The instrument's type value and data representing the
            instrument, as a pair.

        :rtype: ``(type, data)``, where ``type`` is of type :py:class:`int` and
            ``data`` is of type :py:class:`bytes`

        :raises ValueError: if there are more than 8 regions in
            :py:attr:`regions`


.. py:class:: RegionalInstrument.Region(lastPitch, noteDefinition)

    A region within a regional instrument. The highest pitch included in the
    region is :py:attr:`lastPitch`. The lowest pitch included in the region is
    0 if this is the first region in the instrument, or 1 + the
    :py:attr:`lastPitch` of the previous region if it is not.

    :param lastPitch: The initial value for the :py:attr:`lastPitch` attribute.

    :param noteDefinition: The initial value for the :py:attr:`noteDefinition`
        attribute.

    .. py:attribute:: lastPitch

        The highest pitch value included in this region.

        This is measured in half-steps; 60 is middle C. Valid values are
        between 0 and 127, inclusive.

        :type: :py:class:`int`

    .. py:attribute:: noteDefinition

        The note definition that will be used to play notes within this region.

        :type: :py:class:`NoteDefinition`


.. py:function:: instrumentClass(type)

    A convenience function that returns the :py:class:`Instrument` subclass
    that should be used to load an instrument with the given type value.

    :param int type: The type value to find the class for.

    :returns: The class object or ``None``:

        *   ``None``, if ``type`` is :py:const:`NO_INSTRUMENT_TYPE` (0)
        *   :py:class:`SingleNoteInstrument`, if ``type`` is
            :py:const:`SINGLE_NOTE_PCM_INSTRUMENT_TYPE` (1),
            :py:const:`SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE` (2),
            :py:const:`SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE` (3),
            or any other value less than 16
        *   :py:class:`RangeInstrument`, if ``type`` is
            :py:const:`RANGE_INSTRUMENT_TYPE` (16)
        *   :py:class:`RegionalInstrument`, if ``type`` is
            :py:const:`REGIONAL_INSTRUMENT_TYPE` (17)

    :rtype: :py:class:`int`

    :raises ValueError: if ``type`` is larger than 17


.. py:function:: guessInstrumentType(data, startOffset, possibleTypes, bytesAvailable)

    Try to guess the type of instrument stored in some binary data based on
    both the data and a set of possible types (ones that haven't been ruled out
    by the instrument's position in the surrounding data). This function is
    entirely based on heuristics, so it may return different answers for
    similar data, and it cannot always be accurate.

    Types 1, 2 and 3 (:py:const:`SINGLE_NOTE_PCM_INSTRUMENT_TYPE`,
    :py:const:`SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE`, and
    :py:const:`SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE`) are
    considered equivalent by this function, since they are very similar and all
    use the same Python class (:py:class:`SingleNoteInstrument`).

    ``None`` will be returned if it's very unlikely that there is an instrument
    at that position.

    :param bytes data: The data to be read. The possible instrument data need
        not be at the beginning of it.

    :param int startOffset: The offset in the data where the possible
        instrument data begins. This is not the place in the *SBNK* where the
        instrument type value is (as then this function would be trivial);
        rather, it is the place pointed to by the offset that comes just after
        that.

    :param possibleTypes: The set of possible instrument types that should be
        considered.

        :py:const:`SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE` and
        :py:const:`SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE` are both
        treated as aliases of
        :py:const:`SINGLE_NOTE_PCM_INSTRUMENT_TYPE`.

    :type possibleTypes: :py:class:`set` of :py:class:`int`, or
        :py:class:`list` of :py:class:`int`

    :param int bytesAvailable: The number of bytes that are available for a
        possible instrument to occupy. This lets the function rule out
        instrument types that would be too long and overlap the following
        instrument.

    :returns: The best guess for the instrument type value, or ``None`` if it
        seems unlikely that there is any instrument in the data there.

    :rtype: :py:class:`int` or ``None``


.. py:class:: SBNK([file[, unk02[, waveArchiveIDs]]])

    A *SBNK* instrument bank file. This defines a set of instruments that
    sequences and sequence archives can use.

    :param bytes file: The data to be read as an *SBNK* file. If this is not
        provided, the *SBNK* object will initially be empty.

    :param unk02: The initial value for the :py:attr:`unk02` attribute.

    :param waveArchiveIDs: The initial value for the :py:attr:`waveArchiveIDs`
        attribute.

        There can be up to four IDs here. You may include ``None``\s to pad the
        list length to four, but they will be removed.

    .. py:attribute:: dataMergeOptimizationID

        When saving a *SDAT* file containing multiple *SBNK* files, ndspy will
        check if any of them save to identical data. If it finds any, it will
        only encode the data for them once and then reference it multiple
        times, to save some space. This attribute is an extra field that is
        also compared between *SBNK* files, which you can use to exclude
        particular ones from this optimization.

        Since this defaults to 0 for all *SBNK*\s created from scratch, this
        optimization will happen by default. It's unlikely that you will need
        to use this attribute to disable the optimization, but you can.

        .. note::

            This value is not explicitly saved in the *SBNK* file or in the
            *SDAT* file containing it.

        :type: :py:class:`int`

    .. py:attribute:: inaccessibleInstruments

        Some *SBNK* files contain data for instruments that aren't defined
        anywhere in the instrument table. For maximum accuracy, ndspy attempts
        to find and load these instruments using heuristics, so they can be
        included with the file when it is re-saved. These instruments can be
        found here.

        Each dictionary key is the ID of the previous instrument that does have
        an ID, and each dictionary value is the list of inaccessible
        instruments that follow that one.

        This may be more clear with an example:

        Suppose there exists data for two inaccessible instruments between the
        data for instruments 12 and 7 (which is a very possible scenario, since
        instrument data usually does not follow instrument ID order). Call them
        ``inst1`` and ``inst2``. In this example,
        :py:attr:`inaccessibleInstruments` would contain the following:

        .. code-block:: python

            {12: [inst1, inst2]}

        This is read as "the two inaccessible instruments following the data
        for instrument 12 are ``inst1`` and ``inst2``".

        Since this attribute is mostly based on heuristics, it may miss
        instruments, or contain instruments of the wrong type.

        .. warning::
            
            While it is possible to put new instruments here, this is strongly
            recommended against, since it cannot be guaranteed that such
            instruments will be parsed correctly when the *SBNK* is saved and
            re-opened. Additionally, other tools that support *SBNK* may
            corrupt or remove this data. Also, why would you even do that?

            You should either ignore this attribute, or treat it as read-only
            (although it's fine to manually clear it if you want to ensure that
            your files will be as small as possible). In all cases, take
            whatever you find within it with a grain of salt.

            In addition, this attribute may disappear in future versions of
            ndspy if it is discovered that these instruments do have an actual
            purpose.

        :type: :py:class:`dict`: ``{previousID: instruments}``, where
            ``previousID`` is of type :py:class:`int` or ``None``, and
            ``instruments`` is a :py:class:`list` of instances of subclasses of
            :py:class:`Instrument`

        :default: ``{}``

    .. py:attribute:: instruments

        The list of instruments contained in the *SBNK*. "Instrument IDs" are
        indices into this list.

        :type: :py:class:`list` both of instances of subclasses of
            :py:class:`Instrument`, and of ``None``

        :default: ``[]``

    .. py:attribute:: unk02

        The value following the *SBNK*'s file ID in the "INFO" section of the
        *SDAT* file it is contained in. Its purpose is unknown.

        .. note::

            This value is not explicitly saved in the *SBNK* file, but it is
            saved in the *SDAT* file if the *SBNK* is within one.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: waveArchiveIDs

        The list of *SWAR* IDs that instruments in this bank may use. This can
        contain up to four IDs.

        If this *SBNK* is loaded through a sound group entry with its
        :py:attr:`ndspy.soundGroup.GroupEntry.loadSBNKSWARsFrom` attribute set
        to :py:data:`ndspy.soundGroup.SWARLoadMethod.fileIDs`, the IDs in this
        list will be interpreted as raw *SDAT* file IDs instead of *SWAR* IDs.

        .. note::

            ndspy doesn't expose raw *SDAT* file IDs, and the functionality
            described above seems to never really be used in practice (and
            there's honestly no good reason to do so), so you don't really need
            to worry about that case very much.

        :type: :py:class:`list` of :py:class:`int` (4 elements maximum)

        :default: ``[]``

    .. py:classmethod:: fromInstruments(instruments[, unk02[, waveArchiveIDs]])

        Create a *SBNK* from a list of instruments.

        :param instruments: The initial value for the :py:attr:`instruments`
            attribute.

        :param unk02: The initial value for the :py:attr:`unk02` attribute.

        :param waveArchiveIDs: The initial value for the
            :py:attr:`waveArchiveIDs` attribute.

            There can be up to four IDs here. You may include ``None``\s to pad
            the list length to four, but they will be removed.

        :returns: The *SBNK* object.
        :rtype: :py:class:`SBNK`

    .. py:classmethod:: fromFile(filePath[, ...])

        Load an *SBNK* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *SBNK* file to open.
        :type filePath: :py:class:`str` or other path-like object

        Further parameters are the same as those of the default constructor.

        :returns: The *SBNK* object.
        :rtype: :py:class:`SBNK`

    .. py:function:: save()

        Generate file data representing this *SBNK*, and then return that data,
        :py:attr:`unk02`, and :py:attr:`waveArchiveIDs` as a triple. This
        matches the parameters of the default class constructor.

        :returns: The *SBNK* file data, :py:attr:`unk02`, and
            :py:attr:`waveArchiveIDs`.

        :rtype: ``(data, unk02, waveArchiveIDs)``, where ``data`` is of type
            :py:class:`bytes`, ``unk02`` is of type :py:class:`int`, and
            ``waveArchiveIDs`` is a :py:class:`list` of :py:class:`int`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *SBNK*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *SBNK* file to save to.
        :type filePath: :py:class:`str` or other path-like object
