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

``ndspy.soundSequence``: Sound Sequences
========================================

.. module:: ndspy.soundSequence

The ``ndspy.soundSequence`` module  contains classes and enumerations related
to *SSEQ* sound seqeuence files and sound sequence events. If you're interested
in *SSAR* sound sequence archive files, you'll need to use
:py:mod:`ndspy.soundSequenceArchive` in addition to this one.

Sound sequences are conceptually similar to `MIDI files
<https://en.wikipedia.org/wiki/MIDI>`_. A sound sequence is essentially just a
list of "events." Notes are the most common type of event, but there are also a
wide variety of events that can change things like volume, panning, and flow of
control.

Documentation for sequence event classes can be found on the
:doc:`sequenceEvents` page.

.. note::
    While the terms "channel" and "track" are often used interchangeably in
    other documentation, ndspy consistently uses "channel" to refer to hardware
    channels and "track" to refer to *SSEQ* tracks at the software level, as
    defined by the :py:class:`DefineTracksSequenceEvent`.

.. seealso::
    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.


.. toctree to cause sequenceEvents to be a subpage

.. toctree::
    :maxdepth: 2
    :caption: Subpages

    sequenceEvents


.. _parsed-vs-unparsed-sseqs:

Parsed and Unparsed *SSEQ*\s and *SSAR*\s
-----------------------------------------

In general, *SSEQ* and *SSAR* events data (hereafter referred to as just
"*SSEQ* files", since they're both the same in this regard) cannot always be
represented as a list of event objects. Not only does one encounter the halting
problem because *SSEQ* supports variables and conditional branching, but
sequence events could conceivably use overlapping data (although this has never
actually been seen in practice). This complicates ndspy's efforts to be both
easy-to-use and compatible with a wide range of valid input files.

On one hand, most real-life *SSEQ* files don't have a very complicated
structure, and their events data usually can in fact be represented as a list
of events. Being able to access a *SSEQ*\'s data in this way is very intuitive
and powerful.

On the other hand, ndspy should be useful for editing any valid *SSEQ* file,
including ones with events data too complicated for it to parse correctly. It
should therefore let users see and manipulate the raw binary events data if
they want to, or if it can't be parsed automatically.

To handle this, in ndspy, a *SSEQ* can be in one of two states: "unparsed" or
"parsed." An unparsed *SSEQ* can become parsed, but once a *SSEQ* has been
parsed, it cannot go back to being unparsed.

A *SSEQ* loaded from file data (including file data within a *SDAT*) will
initially be "unparsed." At this stage, ndspy has not yet attempted to parse
the events data, and that data can be found in the ``.eventsData`` attribute.

If you want to access events data as a list, you need to call the
``.parse()`` function on the *SSEQ* to switch it to the "parsed" state. This
function (largely powered by :py:func:`readSequenceEvents`) attempts to
parse the events data; if it's succcessful, the events will be placed in the
``.events`` attribute. The function is pretty intelligent, but it nevertheless
has a relatively high failure rate due to the sheer complexity of events data,
so it's good practice to wrap the call in a ``try:``/``except Exception:``
block. If it throws an exception, the *SSEQ* will remain in the unparsed state.

You can check the state of a *SSEQ* using the ``.parsed`` attribute.

Once a *SSEQ* has been parsed, it can never be unparsed (at least not
directly), and ``.eventsData`` becomes inaccessible. If you really need
to work with binary event data from a parsed *SSEQ*, a technique that might
work for you is to call ``.save()`` and then create a new :py:class:`SSEQ` (or
:py:class:`SSAR`) object from the resulting file data. Be aware, though, that
there's no guarantee that saving an unmodified *SSEQ* will reproduce the
original file data exactly, especially if it's been parsed.


.. _multi-track-sseqs:

Multi-track Sequences
---------------------

An *SSEQ* or *SSAR* sequence can have up to 16 tracks. The game will
automatically begin executing the sequence event data at the very beginning
(or, for *SSAR*\s, at whichever event the sequence indicates) on track 0.

If you intend to use more than one track, you must have a
:py:class:`DefineTracksSequenceEvent` as the first event in your sequence. This
declares all of the track IDs you intend to use. This should be followed by one
:py:class:`BeginTrackSequenceEvent` per track (except for track 0), all in a
row, which state where the events for each track begin in the events list.

Since track 0 is the default track which is executing all of these
track-definition events, don't add a :py:class:`BeginTrackSequenceEvent`
for it -- just put its events starting immediately after the final
:py:class:`BeginTrackSequenceEvent`.


.. _sseq-variables:

Sequence Variables
------------------

The sequence player for *SSEQ* and *SSAR* keeps track of an array of 16-bit
[1]_ signed [2]_ integers [3]_ that you can use for whatever you like. These
are known as sequence variables (or just "variables"), and are referenced by ID
number (array index).

You can use the following sequence events to perform mathematical operations on
variables:

*   ``(variable) = value``: :py:class:`VariableAssignmentSequenceEvent`
*   ``(variable) += value``: :py:class:`VariableAdditionSequenceEvent`
*   ``(variable) -= value``: :py:class:`VariableSubtractionSequenceEvent`
*   ``(variable) *= value``: :py:class:`VariableMultiplicationSequenceEvent`
*   ``(variable) /= value``: :py:class:`VariableDivisionSequenceEvent`
*   :py:class:`VariableShiftSequenceEvent`
*   :py:class:`VariableRandSequenceEvent`
*   :py:class:`VariableUnknownB7SequenceEvent`

Once you have values in variables, there are two [4]_ primary ways you can use
them:

Using Variable Values as Sequence Event Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:class:`FromVariableSequenceEvent` lets you use a variable's value as the
last argument to some other sequence event.

Conditional Execution
^^^^^^^^^^^^^^^^^^^^^

In addition to variables, the sequence player also keeps track of a conditional
flag that can be used to skip over certain sequence events. The following
sequence events update the conditional flag:

*   ``condFlag = ((variable) == value)``
    :py:class:`VariableEqualSequenceEvent`
*   ``condFlag = ((variable) >= value)``
    :py:class:`VariableGreaterThanOrEqualSequenceEvent`
*   ``condFlag = ((variable) > value)``
    :py:class:`VariableGreaterThanSequenceEvent`
*   ``condFlag = ((variable) <= value)``
    :py:class:`VariableLessThanOrEqualSequenceEvent`
*   ``condFlag = ((variable) < value)``
    :py:class:`VariableLessThanSequenceEvent`
*   ``condFlag = ((variable) != value)``
    :py:class:`VariableNotEqualSequenceEvent`

After running one of these, you can use an :py:class:`IfSequenceEvent` to
perform conditional execution -- the sequence event immediately following the
:py:class:`IfSequenceEvent` will be skiped if the conditional flag is false.

.. todo::

    How many variables exist?

    Can we double-check that variables are per-sequence rather than per-track?

    How about the conditional flag?


.. [1]
    This has been proven by checking that ``0xFFFF + 1 == 0``.


.. [2]
    This has been proven by checking that ``1 - 2 < 0``.


.. [3]
    This has been proven by checking that ``(3 / 2) * 2 == 2``.


.. [4]
    There also exists a :py:class:`PrintVariableSequenceEvent`, which is not
    well-understood.



.. py:class:: SSEQ([file[, unk02[, bankID[, volume[, channelPressure[, polyphonicPressure[, playerID]]]]]]])

    A *SSEQ* sequence file. This is a piece of music, usually used for
    background music or jingles (such as the "you died" theme in *New Super
    Mario Bros.*).

    :param bytes file: The data to be read as an *SSEQ* file. If this is not
        provided, the *SSEQ* object will initially be empty.

    :param unk02: The initial value for the :py:attr:`unk02` attribute.

    :param bankID: The initial value for the :py:attr:`bankID` attribute.

    :param volume: The initial value for the :py:attr:`volume` attribute.

    :param channelPressure: The initial value for the
        :py:attr:`channelPressure` attribute.

    :param polyphonicPressure: The initial value for the
        :py:attr:`polyphonicPressure` attribute.

    :param playerID: The initial value for the :py:attr:`playerID` attribute.

    .. py:attribute:: bankID

        The ID of the instrument bank (*SBNK*) that this sequence will use.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: channelPressure

        The channel pressure for the sequence. The exact meaning of this is
        unclear.

        :type: :py:class:`int`

        :default: 64

    .. py:attribute:: dataMergeOptimizationID

        When saving a *SDAT* file containing multiple *SSEQ* files, ndspy will
        check if any of them save to identical data. If it finds any, it will
        only encode the data for them once and then reference it multiple
        times, to save some space. This attribute is an extra field that is
        also compared between *SSEQ* files, which you can use to exclude
        particular ones from this optimization.

        Since this defaults to 0 for all *SSEQ*\s created from scratch, this
        optimization will happen by default. It's unlikely that you will need
        to use this attribute to disable the optimization, but you can.

        .. note::

            This value is not explicitly saved in the *SSEQ* file or in the
            *SDAT* file containing it.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: events

        The list of sequence events contained in this *SSEQ*. This is only
        available in parsed *SSEQ*\s (ones with :py:attr:`parsed` set to
        ``True``).

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSEQ*\s.

            :py:attr:`eventsData` -- the equivalent attribute that is available
            before parsing.

        :type: :py:class:`list` of :py:class:`SequenceEvent`

        :default: ``[]``

    .. py:attribute:: eventsData

        The raw event data contained in this *SSEQ*. This is only available in
        unparsed *SSEQ*\s (ones with :py:attr:`parsed` set to ``False``).

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSEQ*\s.

            :py:attr:`events` -- the equivalent attribute that becomes
            available after parsing.

        :type: :py:class:`bytes`

    .. py:attribute:: parsed

        Whether :py:func:`parse` has ever been called on this *SSEQ* object.
        This determines whether :py:attr:`eventsData` or :py:attr:`events` is
        available.

        This attribute is read-only.

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSEQ*\s.

        :type: :py:class:`bool`

        :default: ``True``

    .. py:attribute:: playerID

        The ID of the sequence player that will be used to play this sequence.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: polyphonicPressure

        The polyphonic pressure for the sequence. The exact meaning of this is
        unclear.

        :type: :py:class:`int`

        :default: 50

    .. py:attribute:: unk02

        The value following the *SSEQ*'s file ID in the "INFO" section of the
        *SDAT* file it is contained in. Its purpose is unknown.

        .. note::

            This value is not explicitly saved in the *SSEQ* file, but it is
            saved in the *SDAT* file if the *SSEQ* is within one.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: volume

        The overall volume of the sequence. This is an integer between 0 and
        127, inclusive. It's a good idea to leave this set to 127 and adjust
        volume using other, more precise methods (such as setting the track
        volume or individual note velocities).

        :type: :py:class:`int`

        :default: 127

    .. py:classmethod:: fromEvents(events[, unk02[, bankID[, volume[, channelPressure[, polyphonicPressure[, playerID]]]]]])

        Create a new *SSEQ* object from a list of sequence events.

        :param events: The list of sequence events in the new *SSEQ*.
        :type events: :py:class:`list` of :py:class:`SequenceEvent`

        :param unk02: The initial value for the :py:attr:`unk02` attribute.

        :param bankID: The initial value for the :py:attr:`bankID` attribute.

        :param volume: The initial value for the :py:attr:`volume` attribute.

        :param channelPressure: The initial value for the
            :py:attr:`channelPressure` attribute.

        :param polyphonicPressure: The initial value for the
            :py:attr:`polyphonicPressure` attribute.

        :param playerID: The initial value for the :py:attr:`playerID`
            attribute.

    .. py:classmethod:: fromFile(filePath[, ...])

        Load an *SSEQ* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *SSEQ* file to open.
        :type filePath: :py:class:`str` or other path-like object

        Further parameters are the same as those of the default constructor.

        :returns: The *SSEQ* object.
        :rtype: :py:class:`SSEQ`

    .. py:function:: parse()

        Attempt to process :py:attr:`eventsData` to create :py:attr:`events`.
        If successful, this switches the *SSEQ* from the unparsed to the parsed
        state (see :ref:`parsed-vs-unparsed-sseqs` for a more detailed
        explanation).

        Parsing events data is complex and even completely impossible in some
        cases. If unsuccessful, this function will raise an exception and the
        *SSEQ* will remain in the unparsed state.

        This function is idempotent, meaning that calling it on a *SSEQ*
        already in the parsed state will do nothing.

    .. py:function:: save()

        Generate file data representing this *SSEQ*, and then return that data,
        :py:attr:`unk02`, :py:attr:`bankID`, :py:attr:`volume`,
        :py:attr:`channelPressure`, :py:attr:`polyphonicPressure`, and
        :py:attr:`playerID` as a 7-tuple. This matches the parameters of the
        default class constructor.

        :returns: The *SSEQ* file data, :py:attr:`unk02`, :py:attr:`bankID`,
            :py:attr:`volume`, :py:attr:`channelPressure`,
            :py:attr:`polyphonicPressure`, and :py:attr:`playerID`.

        :rtype: ``(data, unk02, bankID, volume, channelPressure,
            polyphonicPressure, playerID)``, where ``data`` is of type
            :py:class:`bytes` and all of the other elements are of type
            :py:class:`int`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *SSEQ*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *SSEQ* file to save to.
        :type filePath: :py:class:`str` or other path-like object


.. py:function:: printSequenceEventList(events[, labels[, linePrefix]])

    Produce a string representation of a list of sequence events. You can
    optionally provide a dictionary of labels to mark certain events, and a
    prefix string that will be prepended to every line.

    .. note::
        This is a relatively low-level function, mainly intended to power
        :py:class:`SSEQ` and :py:class:`ndspy.soundSequenceArchive.SSAR`. If
        you're using those classes, you can simply call the ``str()`` function
        on them to get a nice printout of their contents instead of calling
        this function directly.

    :param events: The sequence events to be printed.
    :type events: :py:class:`list` of :py:class:`SequenceEvent`

    :param labels: A dictionary containing any labels you would like to apply
        to particular events in the output string. If you specify multiple
        labels for the same event, all of them will be included. You can also
        provide entries with values set to ``None``; these labels will be
        included in the output without pointing to any event.

        :default: ``{}``

    :type labels: :py:class:`dict`: ``{name: event}`` (where ``name`` is of
        type :py:class:`str` and ``event`` is of type
        :py:class:`SequenceEvent`)

    :param linePrefix: A string that will be prepended to every line in the
        output string. (This is mainly useful for indenting the string.)

        :default: ``''``

    :type linePrefix: :py:class:`str`

    :returns: A string representing the list of sequence events.

    :rtype: :py:class:`str`


.. py:function:: readSequenceEvents(data[, notableOffsets])

    Convert raw sequence event data (as seen in *SSEQ* and *SSAR* files) to a
    list of :py:class:`SequenceEvent` objects. This is the inverse of
    :py:func:`saveSequenceEvents`.

    A second list will also be returned that contains the elements from the
    first list that appeared in the input data at the offsets given in
    ``notableOffsets``. This is useful if the data can be played from multiple
    different starting offsets, as is the case with *SSAR* files. It is safe to
    assume that every element of this second list is also an element of the
    first list, and that the length of the second list will match the length of
    ``notableOffsets``.

    .. note::
        This is a relatively low-level function. Most of the time, you should
        use the :py:class:`SSEQ` and
        :py:class:`ndspy.soundSequenceArchive.SSAR` classes, which call this
        function for you in their respective ``parse()`` methods.

    .. warning::
        Parsing events data into a list of event objects is complex, and even
        completely impossible in some extreme cases. As such, you should wrap
        calls to this function in ``try``/``except Exception:`` blocks, and
        implement fallback strategies in case the call fails.

    :param bytes data: The raw sequence events data.

    :param notableOffsets: A list of offsets into the data that point to
        sequence events you'd like to receive references to.

        :default: ``[]``

    :type notableOffsets: :py:class:`list` of :py:class:`int`

    :returns: A list of sequence events that represents the data, and a list
        containing references to the event objects that were indicated in the
        ``notableOffsets`` argument.

    :rtype: ``(events, notableEvents)``, where both elements are
        :py:class:`list`\s of :py:class:`SequenceEvent`


.. py:function:: saveSequenceEvents(events[, notableEvents])

    Convert a list of :py:class:`SequenceEvent` objects to raw sequence event
    data. This is the inverse of :py:func:`readSequenceEvents`.

    A second list will also be returned that contains the offsets in the output
    data of the elements from ``notableEvents``. This is useful if the data can
    be played from multiple different starting points, as is the case with
    *SSAR* files. Every element of ``notableEvents`` must also appear in
    ``events``. It is safe to assume that the length of the second list will
    match the length of ``notableEvents``.

    .. note::
        This is a relatively low-level function. Most of the time, you should
        use the :py:class:`SSEQ` and
        :py:class:`ndspy.soundSequenceArchive.SSAR` classes, which call this
        function for you in their respective ``save()`` methods.

    :param events: The sequence events to be saved.
    :type events: :py:class:`list` of :py:class:`SequenceEvent`

    :param notableEvents: A list of sequence events in ``events`` for which you
        would like to know the offsets in the output data.

        :default: ``[]``

    :type notableEvents: :py:class:`list` of :py:class:`SequenceEvent`

    :returns: The raw sequence event data, and a list containing offsets into
        it that point to the events given in the ``notableEvents`` argument.

    :rtype: ``(data, notableOffsets)``, where ``data`` is of type
        :py:class:`bytes` and ``notableOffsets`` is a :py:class:`list` of
        :py:class:`int`
