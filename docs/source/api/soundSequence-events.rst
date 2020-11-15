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

Sequence Events
===============

.. py:currentmodule:: ndspy.soundSequence

This page describes the sequence event classes within
:py:mod:`ndspy.soundSequence`. All are subclasses of :py:class:`SequenceEvent`.


.. py:class:: SequenceEvent(type)

    An abstract base class representing any sequence event in a *SSEQ* or
    *SSAR* file. This class should not be used directly; it just defines a
    consistent interface for sequence event classes.

    :param type: The initial value for the :py:attr:`type` attribute.

    .. py:attribute:: dataLength

        The number of bytes this sequence event would take if it were to be
        saved (:py:func:`save`) right now. Some subclasses' data lengths depend
        on the specific values of their other attributes; for such classes,
        this attribute may actually be a dynamic property.

        :type: :py:class:`int`

        :default: 1

    .. py:attribute:: type

        This sequence event's "type" value. In general, this identifies a
        sequence event's class (although :py:class:`NoteSequenceEvent` in
        particular can use a variety of type values).

        :type: :py:class:`int`

    .. py:classmethod:: fromData(type, data[, startOffset])

        Create an instance of the :py:class:`SequenceEvent` subclass this
        function is called on, using a particular type value and reading data
        beginning at some offset.

        This base class implementation simply raises
        :py:exc:`NotImplementedError`. All subclasses that can override it,
        should. Some, such as :py:class:`JumpSequenceEvent`, would need more
        information about context than this function's parameters provide, and
        thus must be created using different means.

        :param type: The initial value for the :py:attr:`type` attribute.

        :param bytes data: The data to read from, which contains the data for
            this sequence event.

        :param int startOffset: The offset in ``data`` to begin reading at.
            This should point to the byte containing the event's type value.

            :default: 0

        :returns: A sequence event representing the data.

        :rtype: Subclass of :py:class:`SequenceEvent`

    .. py:function:: save([eventsToOffsets])

        Generate data representing this sequence event. This base class
        implementation simply returns a single byte containing :py:attr:`type`.
        Subclasses should reimplement this function to append their own data to
        this byte.

        :param eventsToOffsets: A dictionary mapping other sequence events in
            the same file as this one to offsets. This can be necessary for
            certain events that reference other events to be able to save
            themselves.

            :default: ``{}``

        :type eventsToOffsets: :py:class:`dict`: ``{event: offset}`` (where
            ``event`` is of type :py:class:`SequenceEvent` and ``offset`` is of
            type :py:class:`int`)

        :returns: Data representing this sequence event.

        :rtype: :py:class:`bytes`


.. py:class:: NoteSequenceEvent(type, velocityAndFlag, duration)

    :base class: :py:class:`SequenceEvent`

    A sequence event that plays a note defined in a sound bank.

    This class represents sequence event types 0x00 through 0x7F; the type
    value actually determines the pitch. (For convenience, then,
    :py:attr:`type` is aliased as :py:attr:`pitch`.)

    :param type: The initial value for the :py:attr:`type` attribute.

    :param int velocityAndFlag: Contains the initial values for the
        :py:attr:`velocity` and :py:attr:`unknownFlag` attributes.
        :py:attr:`velocity` will be set to ``velocityAndFlag & 0x7F``, and
        :py:attr:`unknownFlag` will be set to ``bool(velocityAndFlag & 0x80)``.

    :param duration: The initial value for the :py:attr:`duration` attribute.

    .. py:attribute:: duration

        The amount of time this note should be played for. The units depend on
        the tempo the song is currently being played at. Setting this to 0 will
        cause the note to play forever, until forcibly stopped by something
        else.

        :type: :py:class:`int`

    .. py:attribute:: name

        A human-readable name of this note's pitch, such as ``"F#"``. Note
        names in this attribute may indicate the octave in some way. This is a
        read-only property.

        .. warning::

            The representation of note names used in this attribute may be
            changed in the future. If you want human-readable note names that
            are guaranteed to be consistent across ndspy updates, please write
            your own code for generating them.

        :type: :py:class:`str`

    .. py:attribute:: pitch

        The pitch this note should be played at. Valid values are between 0 and
        127, inclusive. 60 conventionally represents middle C.

        .. seealso:

            :py:attr:`type` -- an alias for this attribute with a name that
            makes more sense in some contexts.

        :type: :py:class:`int`

    .. py:attribute:: type

        This sequence event's "type" value. Valid values for note sequence
        events are between 0 and 127, inclusive. The choice of type value in
        that range determines the note's pitch.

        .. seealso:

            :py:attr:`pitch` -- an alias for this attribute with a name that
            makes more sense in some contexts.

        :type: :py:class:`int`

    .. py:attribute:: unknownFlag

        A flag with an unknown purpose that seems to produce glitchy behavior.
        Notes with this flag set may continue playing after their
        :py:attr:`duration` is over, or do other odd things. Accordingly, you
        should set this to ``False`` unless you have a very good reason not to.

        .. note::

            This value represents the most significant bit of the byte
            containing the :py:attr:`velocity` value.

        :type: :py:class:`bool`

    .. py:attribute:: velocity

        The volume this sequence event should be played at. Valid values are
        between 0 and 127, inclusive. If you're unsure, 127 is generally a good
        choice.

        .. note::

            The most significant bit of the byte containing this value can be
            found in the :py:attr:`unknownFlag` attribute.

        :type: :py:class:`int`


.. py:class:: RestSequenceEvent(duration)

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes *SSEQ* execution to pause for some amount of
    time before moving on. This is sequence event type 0x80.

    :param duration: The initial value for the :py:attr:`duration` attribute.

    .. py:attribute:: duration

        The amount of time the rest will take. The units depend on the tempo
        the song is currently being played at.

        :type: :py:class:`int`


.. py:class:: InstrumentSwitchSequenceEvent(bankID, instrumentID)

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes the track it's placed in to switch to using a
    different instrument (possibly in a different *SBNK*). This is sequence
    event type 0x81.

    A track can have multiple of these events located at different times. This
    lets a single track use different instruments at different times, which is
    one way of partially working around the 16-track limit.

    :param bankID: The initial value for the :py:attr:`bankID` attribute.

    :param instrumentID: The initial value for the :py:attr:`instrumentID`
        attribute.

    .. py:attribute:: bankID

        The ID of the *SBNK* file that the desired instrument is located in.
        The *SBNK* needs to already be loaded, or else this track will stop
        playing.

        :type: :py:class:`int`

    .. py:attribute:: instrumentID

        The ID of the instrument within the *SBNK* that this track should begin
        using.

        :type: :py:class:`int`


.. py:class:: BeginTrackSequenceEvent(trackNumber, firstEvent)

    :base class: :py:class:`SequenceEvent`

    A sequence event that declares the location in the sequence event
    data at which a particular track should begin executing. This is sequence
    event type 0x93.

    :param trackNumber: The initial value for the :py:attr:`trackNumber`
        attribute.

    :param firstEvent: The initial value for the :py:attr:`firstEvent`
        attribute.

    .. seealso::

        :ref:`multi-track-sseqs` -- for more information about how to use this
        event.

    .. py:attribute:: firstEvent

        A reference to the event at which the track should begin executing.

        .. warning::

            This event *must* appear somewhere in the list of sequence events
            you're building, or else you'll experience errors that prevent you
            from saving your *SSEQ* or *SSAR*!

        :type: :py:class:`SequenceEvent`

    .. py:attribute:: trackNumber

        The ID of the track number that this event is referring to. This track
        should have already been defined with a
        :py:class:`DefineTracksSequenceEvent` earlier in the sequence.

        :type: :py:class:`int`


.. py:class:: JumpSequenceEvent(destination)

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes execution of the current track to jump to some
    other location. This is sequence event type 0x94.

    These are often used to create sequences that loop infinitely.

    :param destination: The initial value for the :py:attr:`destination`
        attribute.

    .. seealso::

        :py:class:`CallSequenceEvent` -- a similar event that also pushes the
        current event's address to a return-address stack.

    .. py:attribute:: destination

        A reference to the event that execution should jump to.

        .. warning::

            This event *must* appear somewhere in the list of sequence events
            you're building, or else you'll experience errors that prevent you
            from saving your *SSEQ* or *SSAR*!

        :type: :py:class:`SequenceEvent`


.. py:class:: CallSequenceEvent(destination)

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes execution of the current track to jump to some
    other location, and pushes the current event's address to a return-address
    stack. This is sequence event type 0x95.

    This can be used with :py:class:`ReturnSequenceEvent` to implement
    function calls.

    :param destination: The initial value for the :py:attr:`destination`
        attribute.

    .. seealso::

        :py:class:`JumpSequenceEvent` -- a similar event that does not affect
        the return-address stack.

    .. py:attribute:: destination

        A reference to the event that execution should jump to.

        .. warning::

            This event *must* appear somewhere in the list of sequence events
            you're building, or else you'll experience errors that prevent you
            from saving your *SSEQ* or *SSAR*!

        :type: :py:class:`SequenceEvent`


.. py:class:: RandomSequenceEvent(subType, args, randMin, randMax)

    :base class: :py:class:`SequenceEvent`

    A sequence event that executes some other event with a randomized last
    argument. This is sequence event type 0xA0.

    This is a complicated sequence event. Set :py:attr:`subType` to the type
    value of some other sequence event, which will be executed with a
    randomized last argument. Then put all of the arguments except for the last
    one into :py:attr:`args`. Finally, use :py:attr:`randMin` and
    :py:attr:`randMax` to choose the minimum and maximum values for the
    randomized last argument.

    :param subType: The initial value for the :py:attr:`subType` attribute.

    :param args: The initial value for the :py:attr:`args` attribute.

    :param randMin: The initial value for the :py:attr:`randMin` attribute.

    :param randMax: The initial value for the :py:attr:`randMax` attribute.

    .. todo::

        This information is based on some variable names from *sseq2mid*\'s
        source code, and on a few examples studied in a hex editor. This event
        should really be tested more carefully.

    .. py:attribute:: subType

        The type value of the sequence event that will be executed.

        :type: :py:class:`int`

    .. py:attribute:: args

        The arguments to the sequence event, except for the last one.

        :type: :py:class:`list` of :py:class:`int`

    .. py:attribute:: randMin

        The minimum value that can be chosen for the randomized last argument.

        :type: :py:class:`int`

    .. py:attribute:: randMax

        The maximum value that can be chosen for the randomized last argument.

        .. todo::

            Is this inclusive or exclusive?

        :type: :py:class:`int`


.. py:class:: FromVariableSequenceEvent(subType, variableID[, unknown])

    :base class: :py:class:`SequenceEvent`

    A sequence event that executes some other event with its last argument
    taken from a variable. This is sequence event type 0xA1.

    This is a complicated sequence event. Set :py:attr:`subType` to the type
    value of some other sequence event, which will be executed with its last
    argument taken from a variable. Then put the variable ID that will contain
    the desired value into :py:attr:`variableID`.

    :param subType: The initial value for the :py:attr:`subType` attribute.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param unknown: The initial value for the :py:attr:`unknown` attribute.

    .. todo::

        This sequence event is in serious need of further research.

    .. py:attribute:: subType

        The type value of the sequence event that will be executed.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The game will use the value contained in the variable specified here as
        the last argument to the sequence event.

        :type: :py:class:`int`

    .. py:attribute:: unknown

        No idea what this is. According to *sseq2mid*, this is only present in
        the data if :py:attr:`subType` is between 0xB0 and 0xBD?

        :type: :py:class:`int`

        :default: ``None``


.. py:class:: IfSequenceEvent()

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes the next event to be skipped if the
    conditional flag is currently false. This is sequence event type 0xA2.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.


.. py:class:: VariableAssignmentSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets a variable to a given value. This is sequence
    event type 0xB0.

    This essentially does ``(variable) = value``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to set the variable to.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that the value will be put into.

        :type: :py:class:`int`


.. py:class:: VariableAdditionSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that increments a variable by a given value. This is
    sequence event type 0xB1.

    This essentially does ``(variable) += value``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        How much to increment the variable's value.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that will be incremented.

        :type: :py:class:`int`


.. py:class:: VariableSubtractionSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that decrements a variable by a given value. This is
    sequence event type 0xB2.

    This essentially does ``(variable) -= value``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        How much to decrement the variable's value.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that will be decremented.

        :type: :py:class:`int`


.. py:class:: VariableMultiplicationSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that multiplies a variable by a given value. This is
    sequence event type 0xB3.

    This essentially does ``(variable) *= value``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The factor to multiply the variable's value by.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that will be multiplied.

        :type: :py:class:`int`


.. py:class:: VariableDivisionSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that divides a variable by a given value. This is
    sequence event type 0xB4.

    This essentially does ``(variable) /= value``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The divisor to divide the variable's value by.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that will be divided.

        :type: :py:class:`int`


.. py:class:: VariableShiftSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that left-shifts a variable by a given value. If the value
    is negative, it is right-shifted (arithmetic, not logical) instead. This is
    sequence event type 0xB4.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The shift amount. Positive values result in left-shift, negative values
        result in arithmetic right-shift.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that will be shifted.

        :type: :py:class:`int`


.. py:class:: VariableRandSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets a variable to a random value between 0 and a
    specified outer limit (inclusive). This is sequence event type 0xB6.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. warning::

        If called soon after the game boots, the ARM7 CPU may have low enough
        entropy that this event will behave deterministically. This is the root
        cause of a bug in *Mario Kart DS* -- the sound effect that plays upon
        game boot is intended to be randomized, but in practice, it always
        selects the same sound on a given DS hardware model.

    .. warning::

        Due to an overflow bug, this event does not work as expected if
        :py:attr:`value` is set to -32768 -- instead of selecting from the
        range [-32768, 0], it uses [0, 32767]. This bug has been verified to
        exist in a selection of games from 2005 to 2012, so it probably affects
        all games.

    .. py:attribute:: value

        The random value chosen at runtime will be between 0 and this value
        (inclusive). This therefore behaves as an upper limit if positive, and
        a lower limit if negative.

        Setting this to -32768 is not recommended; see the warning above.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable that will be set to a random value.

        :type: :py:class:`int`


.. py:class:: VariableUnknownB7SequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    .. deprecated:: 3.0.0

        As code analysis has shown that this sequence event probably never
        existed, this class will be removed in the future.

    A sequence event that has no code associated with it at all (verified in a
    selection of games from 2005 to 2012), and does nothing. This is sequence
    event type 0xB7.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. py:attribute:: value

        A value that does nothing.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable this sequence event will (not) act upon.

        :type: :py:class:`int`


.. py:class:: VariableEqualSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the conditional flag to true if the specified
    variable contains a given value, or to false otherwise. This is sequence
    event type 0xB8.

    This essentially does ``condFlag = ((variable) == value)``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to compare the variable's against.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable to check.

        :type: :py:class:`int`


.. py:class:: VariableGreaterThanOrEqualSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the conditional flag to true if the specified
    variable contains a value greater than or equal to a given value, or to
    false otherwise. This is sequence event type 0xB9.

    This essentially does ``condFlag = ((variable) >= value)``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to compare the variable's against.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable to check.

        :type: :py:class:`int`


.. py:class:: VariableGreaterThanSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the conditional flag to true if the specified
    variable contains a value greater than a given value, or to false
    otherwise. This is sequence event type 0xBA.

    This essentially does ``condFlag = ((variable) > value)``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to compare the variable's against.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable to check.

        :type: :py:class:`int`


.. py:class:: VariableLessThanOrEqualSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the conditional flag to true if the specified
    variable contains a value less than or equal to a given value, or to false
    otherwise. This is sequence event type 0xBB.

    This essentially does ``condFlag = ((variable) <= value)``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to compare the variable's against.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable to check.

        :type: :py:class:`int`


.. py:class:: VariableLessThanSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the conditional flag to true if the specified
    variable contains a value less than a given value, or to false otherwise.
    This is sequence event type 0xBC.

    This essentially does ``condFlag = ((variable) < value)``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to compare the variable's against.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable to check.

        :type: :py:class:`int`


.. py:class:: VariableNotEqualSequenceEvent(variableID, value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the conditional flag to true if the specified
    variable does not contain a given value, or to false otherwise. This is
    sequence event type 0xBD.

    This essentially does ``condFlag = ((variable) != value)``.

    :param variableID: The initial value for the :py:attr:`variableID`
        attribute.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :ref:`sseq-variables` -- for more information about how to use this
        event.

    .. py:attribute:: value

        The value to compare the variable's against.

        :type: :py:class:`int`

    .. py:attribute:: variableID

        The ID of the variable to check.

        :type: :py:class:`int`


.. py:class:: PanSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets `the stereo panning value
    <https://en.wikipedia.org/wiki/Panning_%28audio%29>`_ for the current
    track. This is sequence event type 0xC0.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. note::

        *SBNK* instruments can also specify panning values. The interplay
        between instrument and track panning may cause your track's sounds to
        ultimately be panned differently from how your
        :py:class:`PanSequenceEvent` dictates.

    .. todo::

        Is this actually per-track, or is it global?

    .. py:attribute:: value

        The panning value. A value of 64 is centered. Smaller values pan to the
        left, and larger values pan to the right.

        .. todo::

            This is stored as a byte; what happens if you use values above 127?

        :type: :py:class:`int`


.. py:class:: TrackVolumeSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the volume of the current track. This is
    sequence event type 0xC1.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. py:attribute:: value

        The value to set the track volume to. 0 is silent, and 127 is maximum
        loudness.

        .. todo::

            This is stored as a byte; what happens if you use values above 127?

        :type: :py:class:`int`


.. py:class:: GlobalVolumeSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the global volume, for all tracks. This is
    sequence event type 0xC2.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. py:attribute:: value

        The value to set the global volume to. 0 is silent, and 127 is maximum
        loudness.

        .. todo::

            This is stored as a byte; what happens if you use values above 127?

        :type: :py:class:`int`


.. py:class:: TransposeSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes :py:class:`NoteSequenceEvent`\s following it
    in the current track to be transposed. This is sequence event type 0xC3.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        If I have a :py:class:`ndspy.soundBank.RangeInstrument` with separate
        note definitions for E and F, and I use this sequence event to
        transpose upward one half-step and then play an E, does it play the E
        at a higher pitch, or does it play the F?

    .. todo::

        Is this actually per-track, or is it global?

    .. py:attribute:: value

        A value related to the track transposition.

        .. todo::

            How does this work?

            Here's a guess: 64 is no transposition, and lower values transpose
            downward and higher values transpose upward?

        :type: :py:class:`int`


.. py:class:: PortamentoSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `portamentos
    <https://en.wikipedia.org/wiki/Portamento>`_. This is sequence event type
    0xC4.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to portamentos:
        :py:class:`PortamentoRangeSequenceEvent`,
        :py:class:`PortamentoFromSequenceEvent`,
        :py:class:`PortamentoOnOffSequenceEvent`,
        :py:class:`PortamentoDurationSequenceEvent`,
        :py:class:`TieSequenceEvent`.

    .. todo::

        How does this actually work?

    .. py:attribute:: value

        A value related to the portamento.

        :type: :py:class:`int`


.. py:class:: PortamentoRangeSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `portamentos
    <https://en.wikipedia.org/wiki/Portamento>`_. This is sequence event type
    0xC5.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to portamentos:
        :py:class:`PortamentoSequenceEvent`,
        :py:class:`PortamentoFromSequenceEvent`,
        :py:class:`PortamentoOnOffSequenceEvent`,
        :py:class:`PortamentoDurationSequenceEvent`,
        :py:class:`TieSequenceEvent`.

    .. todo::

        How does this actually work?

    .. py:attribute:: value

        A value related to the portamento.

        :type: :py:class:`int`


.. py:class:: TrackPrioritySequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the priority of the current track. Tracks with
    higher priority values will be favored over those with lower priorities
    if the sound system runs out of hardware channels and needs to cut off some
    sounds early. This is sequence event type 0xC6.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        I haven't tested this very much. Is that explanation accurate? Also,
        what are the minimum and maximum priority values, and what's the
        default? If the valid range isn't 0-255, what happens if you choose a
        priority outside of the range?

    .. py:attribute:: value

        The new priority for the current track.

        :type: :py:class:`int`


.. py:class:: MonoPolySequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that switches the current track to mono mode or poly mode.
    This is sequence event type 0xC7.

    The default mode is mono mode.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        :py:class:`MonoPolySequenceEvent.Value` -- for an explanation about the
        difference between mono and poly mode

    .. py:attribute:: value

        The mode to set the track to.

        :type: :py:class:`MonoPolySequenceEvent.Value` (or :py:class:`int`)


.. py:class:: MonoPolySequenceEvent.Value

    :base class: :py:class:`enum.IntEnum`

    An enumeration that distinguishes between "mono" and "poly" track modes.

    Mono mode is simpler to use, but less powerful. In mono mode,
    :py:class:`NoteSequenceEvent`\s are blocking -- that is, if you play a
    :py:class:`NoteSequenceEvent`, execution will pause on that event until the
    note has finished playing. Thus, in this mode, you can just put a bunch of
    :py:class:`NoteSequenceEvent`\s in a row to play a simple tune. This mode
    is often used in *SSAR* sound effects.

    Poly mode is a bit more complicated, but more flexible. In poly mode,
    :py:class:`NoteSequenceEvent`\s are non-blocking -- that is, if you play a
    :py:class:`NoteSequenceEvent`\, execution will keep going while the note is
    being played. This lets you play multiple notes at once to produce chords.
    In this mode, the only way to cause a delay between events is to use
    :py:class:`RestSequenceEvent`\s. This mode is usually used in *SSEQ* music
    files.

    The default mode is mono mode.

    .. data:: MONO

        Value 1: indicates mono mode.

    .. data:: POLY

        Value 0: indicates poly mode.


.. py:class:: TieSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that enables or disables `"tie"
    <https://en.wikipedia.org/wiki/Tie_(music)>`_ mode on the current track.
    This is sequence event type 0xC8.

    If tie mode is enabled and the track is in mono mode
    (:py:class:`MonoPolySequenceEvent`), consecutive notes
    (:py:class:`NoteSequenceEvent`) will be merged together into one long note.
    This can be used with portamentos to create a note that bends in
    arbitrarily complex ways.

    It's unclear if this can also work correctly in poly mode, or if there are
    more uses for this mode than just portamentos.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to portamentos:
        :py:class:`PortamentoSequenceEvent`,
        :py:class:`PortamentoRangeSequenceEvent`,
        :py:class:`PortamentoFromSequenceEvent`,
        :py:class:`PortamentoOnOffSequenceEvent`,
        :py:class:`PortamentoDurationSequenceEvent`.

    .. py:attribute:: value

        Whether tie mode should be enabled.

        :type: :py:class:`bool` (or :py:class:`int`)


.. py:class:: PortamentoFromSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `portamentos
    <https://en.wikipedia.org/wiki/Portamento>`_. This is sequence event type
    0xC9.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        This needs further testing. Based on some SSARs I looked at (e.g.
        ``SAR_VS_COMMON_MENU`` in NSMB), it appears as though this sets the
        pitch that the next note will bend from (over its entire duration), but
        some tests didn't seem to agree. For what it's worth, this event is
        called "portamento control" by some sources.

    .. seealso::

        Other sequence events related to portamentos:
        :py:class:`PortamentoSequenceEvent`,
        :py:class:`PortamentoRangeSequenceEvent`,
        :py:class:`PortamentoOnOffSequenceEvent`,
        :py:class:`PortamentoDurationSequenceEvent`,
        :py:class:`TieSequenceEvent`.

    .. py:attribute:: value

        A value related to the portamento.

        :type: :py:class:`int`


.. py:class:: VibratoDepthSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `vibratos
    <https://en.wikipedia.org/wiki/Vibrato>`_. This is sequence event type
    0xCA.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to vibratos:
        :py:class:`VibratoSpeedSequenceEvent`,
        :py:class:`VibratoTypeSequenceEvent`,
        :py:class:`VibratoRangeSequenceEvent`,
        :py:class:`VibratoDelaySequenceEvent`.

    .. todo::

        This needs testing. I don't really know how vibrato effects work.

    .. py:attribute:: value

        A value related to the vibrato.

        :type: :py:class:`int`


.. py:class:: VibratoSpeedSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `vibratos
    <https://en.wikipedia.org/wiki/Vibrato>`_. This is sequence event type
    0xCB.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to vibratos:
        :py:class:`VibratoDepthSequenceEvent`,
        :py:class:`VibratoTypeSequenceEvent`,
        :py:class:`VibratoRangeSequenceEvent`,
        :py:class:`VibratoDelaySequenceEvent`.

    .. todo::

        This needs testing. I don't really know how vibrato effects work.

    .. py:attribute:: value

        A value related to the vibrato.

        :type: :py:class:`int`


.. py:class:: VibratoTypeSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the current vibrato type. This is sequence event
    type 0xCC.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        This needs testing. I don't really know how vibrato effects work.

        Also, what's the default vibrato type?

    .. py:attribute:: value

        The new vibrato type.

        :type: :py:class:`VibratoTypeSequenceEvent.Value` (or :py:class:`int`)


.. py:class:: VibratoTypeSequenceEvent.Value

    :base class: :py:class:`enum.IntEnum`

    An enumeration that distinguishes between the types of vibrato effects that
    can be played.

    .. seealso::

        Other sequence events related to vibratos:
        :py:class:`VibratoDepthSequenceEvent`,
        :py:class:`VibratoSpeedSequenceEvent`,
        :py:class:`VibratoRangeSequenceEvent`,
        :py:class:`VibratoDelaySequenceEvent`.

    .. todo::

        What's the default?

    .. data:: PITCH

        Value 0: notes' pitches will be vibrated.

    .. data:: VOLUME

        Value 1: notes' volumes will be vibrated.

    .. data:: PAN

        Value 2: notes' panning values will be vibrated.

        .. seealso::

            :py:class:`PanSequenceEvent` -- for more information about panning.


.. py:class:: VibratoRangeSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `vibratos
    <https://en.wikipedia.org/wiki/Vibrato>`_. This is sequence event type
    0xCD.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to vibratos:
        :py:class:`VibratoDepthSequenceEvent`,
        :py:class:`VibratoSpeedSequenceEvent`,
        :py:class:`VibratoTypeSequenceEvent`,
        :py:class:`VibratoDelaySequenceEvent`.

    .. todo::

        This needs testing. I don't really know how vibrato effects work.

    .. py:attribute:: value

        A value related to the vibrato.

        :type: :py:class:`int`


.. py:class:: PortamentoOnOffSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that enables or disables `portamento
    <https://en.wikipedia.org/wiki/Portamento>`_ mode. This is sequence event
    type 0xCE.

    While a track is in this mode, every note (:py:class:`NoteSequenceEvent`)
    will bend from the previous note's pitch to its own, over its entire
    duration. This is most useful in mono mode, and with
    :py:class:`TieSequenceEvent`\s.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to portamentos:
        :py:class:`PortamentoSequenceEvent`,
        :py:class:`PortamentoRangeSequenceEvent`,
        :py:class:`PortamentoFromSequenceEvent`,
        :py:class:`PortamentoDurationSequenceEvent`,
        :py:class:`TieSequenceEvent`.

    .. py:attribute:: value

        Whether portamento mode should be enabled.

        :type: :py:class:`bool` (or :py:class:`int`)


.. py:class:: PortamentoDurationSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `portamentos
    <https://en.wikipedia.org/wiki/Portamento>`_. This is sequence event type
    0xCF.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to portamentos:
        :py:class:`PortamentoSequenceEvent`,
        :py:class:`PortamentoRangeSequenceEvent`,
        :py:class:`PortamentoFromSequenceEvent`,
        :py:class:`PortamentoOnOffSequenceEvent`,
        :py:class:`TieSequenceEvent`.

    .. todo::

        How does this actually work?

    .. py:attribute:: value

        A value related to the portamento.

        :type: :py:class:`int`


.. py:class:: AttackRateSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the attack rate for notes
    (:py:class:`NoteSequenceEvent`) in the current track. This is sequence
    event type 0xD0.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        `The Wikipedia page on envelope
        <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
        decay, sustain, and release values.

    .. todo::

        How does this actually work? Is this actually per-track, or global? How
        does this relate to the attack rates set in the note definitions?
        What's the default attack rate value?

    .. py:attribute:: value

        A value related to the attack rate.

        :type: :py:class:`int`


.. py:class:: DecayRateSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the decay rate for notes
    (:py:class:`NoteSequenceEvent`) in the current track. This is sequence
    event type 0xD1.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        `The Wikipedia page on envelope
        <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
        decay, sustain, and release values.

    .. todo::

        How does this actually work? Is this actually per-track, or global? How
        does this relate to the decay rates set in the note definitions? What's
        the default decay rate value?

    .. py:attribute:: value

        A value related to the decay rate.

        :type: :py:class:`int`


.. py:class:: SustainRateSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the sustain rate for notes
    (:py:class:`NoteSequenceEvent`) in the current track. This is sequence
    event type 0xD2.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        `The Wikipedia page on envelope
        <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
        decay, sustain, and release values.

    .. todo::

        How does this actually work? Is this actually per-track, or global? How
        does this relate to the sustain rates set in the note definitions?
        What's the default sustain rate value?

    .. py:attribute:: value

        A value related to the sustain rate.

        :type: :py:class:`int`


.. py:class:: ReleaseRateSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the release rate for notes
    (:py:class:`NoteSequenceEvent`) in the current track. This is sequence
    event type 0xD3.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        `The Wikipedia page on envelope
        <https://en.wikipedia.org/wiki/Envelope_(music)>`_ explains attack,
        decay, sustain, and release values.

    .. todo::

        How does this actually work? Is this actually per-track, or global? How
        does this relate to the release rates set in the note definitions?
        What's the default release rate value?

    .. py:attribute:: value

        A value related to the release rate.

        :type: :py:class:`int`


.. py:class:: BeginLoopSequenceEvent(loopCount)

    :base class: :py:class:`SequenceEvent`

    A sequence event that begins a loop in the current track. This is sequence
    event type 0xD4.

    The end of the loop must be marked by an :py:class:`EndLoopSequenceEvent`.

    :param loopCount: The initial value for the :py:attr:`loopCount` attribute.

    .. py:attribute:: loopCount

        The number of times the loop should execute.

        .. todo::

            Or is it the number of times that execution should jump back to the
            beginning of the loop?

        :type: :py:class:`int`


.. py:class:: ExpressionSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    An unknown sequence event type. This is sequence event type 0xD5.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        What on earth is this?

    .. py:attribute:: value

        An unknown value.

        :type: :py:class:`int`


.. py:class:: PrintVariableSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    An unknown sequence event type. This is sequence event type 0xD6.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        What on earth is this?

    .. py:attribute:: value

        An unknown value.

        :type: :py:class:`int`


.. py:class:: VibratoDelaySequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event related to `vibratos
    <https://en.wikipedia.org/wiki/Vibrato>`_. This is sequence event type
    0xE0.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. seealso::

        Other sequence events related to vibratos:
        :py:class:`VibratoDepthSequenceEvent`,
        :py:class:`VibratoSpeedSequenceEvent`,
        :py:class:`VibratoTypeSequenceEvent`,
        :py:class:`VibratoRangeSequenceEvent`.

    .. todo::

        This needs testing. I don't really know how vibrato effects work.

    .. py:attribute:: value

        A value related to the vibrato.

        :type: :py:class:`int`


.. py:class:: TempoSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    A sequence event that sets the tempo for all tracks in the sequence. This
    is sequence event type 0xE1.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. py:attribute:: value

        The new tempo to use.

        .. todo::

            I think this is measured in BPM, but that needs to be
            double-checked.

        :type: :py:class:`int`


.. py:class:: SweepPitchSequenceEvent(value)

    :base class: :py:class:`SequenceEvent`

    An unknown sequence event type. This is sequence event type 0xE3.

    :param value: The initial value for the :py:attr:`value` attribute.

    .. todo::

        What on earth is this?

    .. py:attribute:: value

        An unknown value.

        :type: :py:class:`int`


.. py:class:: EndLoopSequenceEvent()

    :base class: :py:class:`SequenceEvent`

    A sequence event that ends a loop previously begun with a
    :py:class:`BeginLoopSequenceEvent`. This is sequence event type 0xFC.


.. py:class:: ReturnSequenceEvent()

    :base class: :py:class:`SequenceEvent`

    A sequence event that causes execution of the current track to jump back to
    the most recently encountered :py:class:`CallSequenceEvent`. This is
    sequence event type 0xFD.


.. py:class:: DefineTracksSequenceEvent(trackNumbers)

    :base class: :py:class:`SequenceEvent`

    A sequence event that defines the track IDs that will be used in the
    sequence. This is sequence event type 0xFE.

    :param trackNumbers: The initial value for the :py:attr:`trackNumbers`
        attribute.

    .. seealso::

        :ref:`multi-track-sseqs` -- for more information about how to use this
        event.

    .. py:attribute:: trackNumbers

        The set of track IDs that will be used in the sequence, including track
        0. All numbers in this set should be between 0 and 15 inclusive.

        :type: :py:class:`set` of :py:class:`int`


.. py:class:: EndTrackSequenceEvent()

    :base class: :py:class:`SequenceEvent`

    A sequence event that ends execution of the current track. This is sequence
    event type 0xFF.

    When this is encountered, any :py:class:`NoteSequenceEvent`\s that are
    currently playing are stopped immediately. If you're in poly mode (see
    :py:class:`MonoPolySequenceEvent`), you may need to add one last
    :py:class:`RestSequenceEvent` just before the end-track event in order to
    prevent the last note from getting cut off.

    This event is only required if your track is supposed to end after a finite
    amount of time. Tracks that use :py:class:`JumpSequenceEvent` to loop
    infinitely do not need one of these.


.. py:class:: RawDataSequenceEvent(data)

    :base class: :py:class:`SequenceEvent`

    A dummy sequence event that represents raw binary data that seems to be
    unreachable as far as ndspy can tell.

    :param data: The initial value for the :py:attr:`data` attribute.

    .. py:attribute:: data

        The raw binary data this sequence event represents.

        :type: :py:class:`bytes`
