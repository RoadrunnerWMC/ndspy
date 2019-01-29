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

``ndspy.soundSequenceArchive``: Sound Sequence Archives
=======================================================

.. module:: ndspy.soundSequenceArchive

The ``ndspy.soundSequenceArchive`` module lets you work with *SSAR* sound
sequence archive files. These are generally used for sound effects.

.. seealso::

    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <../appendices/sdat-structure>`.

    :py:mod:`ndspy.soundSequence` -- contains sequence event classes, and some
    detailed explanations of how to use them.


.. py:class:: SSAR([file[, unk02[, names]]])

    A *SSAR* sequence archive file. This contains a blob of sequence events
    data, and a list of "sequences" that are essentially just pointers to
    starting locations in that data.

    :param bytes file: The data to be read as an *SSAR* file. If this is not
        provided, the *SSAR* object will initially be empty.

    :param unk02: The initial value for the :py:attr:`unk02` attribute.

    :param names: A list of names for the sequences in the *SSAR*. *SSAR* files
        do not themselves contain names for their sequences, but sequence names
        may be present elsewhere in an *SDAT* file; hence this parameter.

        This will be ignored if ``file`` is not provided. Any sequences that do
        not have names provided here will be given placeholder names.

        :default: ``[]``

    :type names: :py:class:`list` of :py:class:`str`

    .. py:attribute:: dataMergeOptimizationID

        When saving a *SDAT* file containing multiple *SSAR* files, ndspy will
        check if any of them save to identical data. If it finds any, it will
        only encode the data for them once and then reference it multiple
        times, to save some space. This attribute is an extra field that is
        also compared between *SSAR* files, which you can use to exclude
        particular ones from this optimization.

        Since this defaults to 0 for all *SSAR*\s created from scratch, this
        optimization will happen by default. It's unlikely that you will need
        to use this attribute to disable the optimization, but you can.

        .. note::

            This value is not explicitly saved in the *SSAR* file or in the
            *SDAT* file containing it.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: events

        The list of sequence events contained in this *SSAR*, shared by all
        sequences. This is only available in parsed *SSAR*\s (ones with
        :py:attr:`parsed` set to ``True``).

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSAR*\s.

            :py:attr:`eventsData` -- the equivalent attribute that is available
            before parsing.

        :type: :py:class:`list` of
            :py:class:`ndspy.soundSequence.SequenceEvent`

        :default: ``[]``

    .. py:attribute:: eventsData

        The raw event data contained in this *SSAR*, shared by all sequences.
        This is only available in unparsed *SSAR*\s (ones with
        :py:attr:`parsed` set to ``False``).

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSAR*\s.

            :py:attr:`events` -- the equivalent attribute that becomes
            available after parsing.

        :type: :py:class:`bytes`

    .. py:attribute:: parsed

        Whether :py:func:`parse` has ever been called on this *SSAR* object.
        This determines whether :py:attr:`eventsData` or :py:attr:`events` is
        available.

        This attribute is read-only.

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSAR*\s.

        :type: :py:class:`bool`

        :default: ``True``

    .. py:attribute:: sequences

        The sequences in this *SSAR*, in the form of a list of name-value pairs
        containing :py:class:`ndspy.soundSequence.SSARSequence` instances.
        The sequences all share the same pool of events (:py:attr:`eventsData`,
        :py:attr:`events`), and only differ in their starting positions and
        some metadata.

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
            type :py:class:`str` or ``None``, and ``sequence`` is of type
            :py:class:`SSARSequence` or ``None``

        :default: ``[]``

    .. py:attribute:: unk02

        The value following the *SSAR*'s file ID in the "INFO" section of the
        *SDAT* file it is contained in. Its purpose is unknown.

        .. note::

            This value is not explicitly saved in the *SSAR* file, but it is
            saved in the *SDAT* file if the *SSEQ* is within one.

        :type: :py:class:`int`

        :default: 0

    .. py:classmethod:: fromEventsAndSequences(events, sequences[, unk02])

        Create a new *SSAR* object from a list of sequence events and a list of
        sequences.

        :param events: The list of sequence events in the new *SSAR*.
        :type events: :py:class:`list` of
            :py:class:`ndspy.soundSequence.SequenceEvent`

        :param sequences: The list of sequences in the new *SSAR*.
        :type sequences: :py:class:`list` of :py:class:`SSARSequence`

        :param unk02: The initial value for the :py:attr:`unk02` attribute.

    .. py:classmethod:: fromFile(filePath[, ...])

        Load an *SSAR* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *SSAR* file to open.
        :type filePath: :py:class:`str` or other path-like object

        Further parameters are the same as those of the default constructor.

        :returns: The *SSAR* object.
        :rtype: :py:class:`SSAR`

    .. py:function:: parse()

        Attempt to process :py:attr:`eventsData` to create :py:attr:`events`.
        If successful, this switches the *SSAR* from the unparsed to the parsed
        state (see :ref:`parsed-vs-unparsed-sseqs` for a more detailed
        explanation).

        Parsing events data is complex and even completely impossible in some
        cases. If unsuccessful, this function will raise an exception and the
        *SSAR* will remain in the unparsed state.

        This function is idempotent, meaning that calling it on a *SSAR*
        already in the parsed state will do nothing.

    .. py:function:: save()

        Generate file data representing this *SSAR*, and then return that data,
        :py:attr:`unk02`, and a list of sequence names as a triple. This
        matches the parameters of the default class constructor.

        :returns: The *SSAR* file data, :py:attr:`unk02`, and a list of
            sequence names.

        :rtype: ``(data, unk02, names)``, where ``data`` is of type
            :py:class:`bytes`, ``unk02`` is of type :py:class:`int`, and
            ``names`` is a :py:class:`list` of :py:class:`str`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *SSAR*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *SSAR* file to save to.
        :type filePath: :py:class:`str` or other path-like object


.. py:class:: SSARSequence(firstEvent_firstEventOffset[, bankID[, volume[, channelPressure[, polyphonicPressure[, playerID]]]]], *, [parsed=True])

    A sequence within a *SSAR* sequence archive file. These generally contain
    sound effects.

    When created using the default constructor, the sequence will be put into
    the parsed state.

    .. seealso::

        :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining the
        difference between parsed and unparsed *SSAR*\s.

    :param firstEvent_firstEventOffset: The sequence event -- or offset thereof
        -- where the sequence player should begin playing when it plays this
        sequence.

        If ``parsed`` is ``False``, this will be the initial value for the
        :py:attr:`firstEventOffset` attribute.

        If ``parsed`` is ``True``, this will be the initial value for the
        :py:attr:`firstEvent` attribute.

        In either case, ``None`` indicates that the sequence has no event data
        at all; such a sequence will do nothing when played.

    :type firstEvent_firstEventOffset: :py:class:`int` or ``None`` (if
        ``parsed`` is ``False``), or
        :py:class:`ndspy.soundSequence.SequenceEvent` or ``None`` (if
        ``parsed`` is ``True``)

    :param bankID: The initial value for the :py:attr:`bankID` attribute.

    :param volume: The initial value for the :py:attr:`volume` attribute.

    :param channelPressure: The initial value for the
        :py:attr:`channelPressure` attribute.

    :param polyphonicPressure: The initial value for the
        :py:attr:`polyphonicPressure` attribute.

    :param playerID: The initial value for the :py:attr:`playerID` attribute.

    :param parsed: The initial value for the :py:attr:`parsed` attribute.

        :default: ``True``

    .. py:attribute:: bankID

        The ID of the instrument bank (*SBNK*) that this sequence will use.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: channelPressure

        The channel pressure for the sequence. The exact meaning of this is
        unclear.

        :type: :py:class:`int`

        :default: 64

    .. py:attribute:: firstEvent

        A reference to this sequence's first event in its parent *SSAR*'s
        events list (:py:attr:`SSAR.events`). This is only available in parsed
        *SSAR* sequences (ones with :py:attr:`parsed` set to ``True``).

        A value of ``None`` indicates that the sequence has no event data at
        all.

        .. warning::

            This event *must* appear somewhere in the parent *SSAR*'s events
            list (:py:attr:`SSAR.events`), or else you'll experience errors
            that prevent you from saving your *SSAR*!

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSAR*\s.

            :py:attr:`firstEventOffset` -- the equivalent attribute that is
            available before parsing.

        :type: :py:class:`ndspy.soundSequence.SequenceEvent` or ``None``

    .. py:attribute:: firstEventOffset

        The offset at which this sequence's first event is located in its
        parent *SSAR*'s raw event data (:py:attr:`SSAR.eventsData`). This is
        only available in unparsed *SSAR* sequences (ones with
        :py:attr:`parsed` set to ``False``).

        A value of ``None`` (or -1) indicates that the sequence has no event
        data at all.

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSAR*\s.

            :py:attr:`firstEvent` -- the equivalent attribute that becomes
            available after parsing.

        :type: :py:class:`int` or :py:class:`None`

    .. py:attribute:: parsed

        Whether :py:func:`parse` has ever been called on this sequence's parent
        *SSAR* object. This determines whether :py:attr:`firstEventOffset` or
        :py:attr:`firstEvent` is available.

        Unless you're doing something like manually moving a sequence from an
        unparsed *SSAR* to a parsed one, it'd be a good idea to treat this as a
        read-only attribute.

        .. seealso::

            :ref:`parsed-vs-unparsed-sseqs` -- the introductory text explaining
            the difference between parsed and unparsed *SSAR*\s.

        :type: :py:class:`bool`

    .. py:attribute:: playerID

        The ID of the sequence player that will be used to play this sequence.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: polyphonicPressure

        The polyphonic pressure for the sequence. The exact meaning of this is
        unclear.

        :type: :py:class:`int`

        :default: 50

    .. py:attribute:: volume

        The overall volume of the sequence. This is an integer between 0 and
        127, inclusive.

        :type: :py:class:`int`

        :default: 127

    .. py:function:: save()

        Return this *SSAR* sequence's first event or first event offset,
        :py:attr:`bankID`, :py:attr:`volume`, :py:attr:`channelPressure`,
        :py:attr:`polyphonicPressure`, and :py:attr:`playerID` as a 6-tuple.
        This matches the parameters of the default class constructor.

        :returns: The first event (if :py:attr:`parsed` is ``True``) or first
            event offset (if :py:attr:`parsed` is ``False``),
            :py:attr:`bankID`, :py:attr:`volume`, :py:attr:`channelPressure`,
            :py:attr:`polyphonicPressure`, and :py:attr:`playerID`.

        :rtype: ``(firstEvent_firstEventOffset, bankID, volume,
            channelPressure, polyphonicPressure, playerID)``, where
            ``firstEvent_firstEventOffset`` is of type (:py:class:`int` if
            :py:attr:`parsed` is ``False``, or
            :py:class:`ndspy.soundSequence.SequenceEvent` if :py:attr:`parsed`
            is ``True``) or ``None``, and all of the other elements are of type
            :py:class:`int`
