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

``ndspy.soundStreamPlayer``: Sound Stream Players
=================================================

.. module:: ndspy.soundStreamPlayer

The ``ndspy.soundStreamPlayer`` module provides a class that represents a
stream player.

A "stream player" plays *STRM* streamed audio files. The stream player data in
an *SDAT* file defines the channels allotted to it. This lets games use
stream players and sequence players simultaneously while minimizing conflicts
between them.

.. seealso::

    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.


.. py:class:: StreamPlayer([channels])

    A stream player.

    :param channels: The initial value for the :py:attr:`channels` attribute.

    .. py:attribute:: channels

        The hardware channels that this stream player will be allowed to use.
        All numbers in this list should be between 0 and 15 inclusive.

        .. note::

            This is a :py:class:`list` rather than a :py:class:`set` because --
            unlike with :py:class:`ndspy.soundSequencePlayer.SequencePlayer` --
            the order of the values is actually preserved in the *SDAT* file.

        :type: :py:class:`list` of :py:class:`int`

        :default: ``[]``

    .. py:function:: save()

        Return this sequence player's :py:attr:`channels` attribute. This
        matches the parameter of the default class constructor.

        Yes, this is a bit of a pointless function. No, I'm not getting rid of
        it. :)

        :returns: :py:attr:`channels`.

        :rtype: :py:class:`list` of :py:class:`int`
