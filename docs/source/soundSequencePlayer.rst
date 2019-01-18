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

``ndspy.soundSequencePlayer``: Sound Sequence Players
=====================================================

.. module:: ndspy.soundSequencePlayer

The ``ndspy.soundSequencePlayer`` module provides a class that represents a
sequence player.

A "sequence player" can play both *SSEQ* files and *SSAR* sequences. The
sequence player data in an *SDAT* file defines a sequence player's limits for
memory and hardware channel usage. This lets games use multiple sequence
players simultaneously while minimizing conflicts between them.

.. seealso::

    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.


.. py:class:: SequencePlayer([maxSequences[, channels[, heapSize]]])

    A sequence player.

    :param maxSequences: The initial value for the :py:attr:`maxSequences`
        attribute.

    :param channels: The initial value for the :py:attr:`channels` attribute.

    :param heapSize: The initial value for the :py:attr:`heapSize` attribute.

    .. py:attribute:: channels

        The hardware channels that this sequence player will be allowed to use.
        If the player is already using all of its allotted channels and needs
        to play another wave, the one that has been playing for the longest
        will be cut off prematurely to allow the new one to play.

        All numbers in this set should be between 0 and 15 inclusive.

        If this is empty, the allowed channels will be determined at runtime.

        :type: :py:class:`set` of :py:class:`int`

        :default: ``set()``

    .. py:attribute:: heapSize

        The total amount of memory that the sequence player will be allowed to
        use.

        If this is 0, the heap size will be determined at runtime.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: maxSequences

        The maximum number of sequences that this sequence player will be
        allowed to play simultaneously. If the player is requested to play
        another sequence while it is already playing this many of them, the one
        that has been playing for the longest will be cut off prematurely to
        allow the new one to play.

        :type: :py:class:`int`

        :default: 1

    .. py:function:: save()

        Return this sequence player's :py:attr:`maxSequences`,
        :py:attr:`channels`, and :py:attr:`heapSize` as a triple. This matches
        the parameters of the default class constructor.

        :returns: :py:attr:`maxSequences`, :py:attr:`channels`,
            and :py:attr:`heapSize`.

        :rtype: ``(maxSequences, channels, heapSize)``, where ``maxSequences``
            is of type :py:class:`int`, ``channels`` is a :py:class:`set` of
            :py:class:`int`, and ``heapSize`` is of type :py:class:`int`
