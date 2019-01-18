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

``ndspy``: General
==================

.. module:: ndspy

The ``ndspy`` namespace contains functions and classes that don't need
their own modules.


.. py:class:: Processor

    :base class: :py:class:`enum.Enum`

    An enumeration that distinguishes between the Nintendo DS's two processors.

    .. data:: ARM9

        The ARM9 processor. This is the main processor used by the DS.

    .. data:: ARM7

        The ARM7 processor. This is used for less-important tasks, and to play
        GBA games.


.. py:class:: WaveType

    :base class: :py:class:`enum.IntEnum`

    An enumeration that distinguishes between the three types of wave data that
    the Nintendo DS sound hardware understands.

    .. data:: PCM8

        Value 0: signed 8-bit `PCM
        <https://en.wikipedia.org/wiki/Pulse-code_modulation>`_ wave data. One
        byte per sample, with 0 being the center line.

    .. data:: PCM16

        Value 1: signed 16-bit little-endian `PCM
        <https://en.wikipedia.org/wiki/Pulse-code_modulation>`_ wave data. Two
        bytes per sample, with 0 being the center line.

    .. data:: ADPCM

        Value 2: little-endian `IMA-ADPCM
        <https://en.wikipedia.org/wiki/Adaptive_differential_pulse-code_modulation>`_
        wave data. This is the most complicated format of the three, but it
        stores about two samples per byte, so it's the most space-efficient
        choice.

        .. seealso::

            More information about IMA-ADPCM, including the quirks of how it's
            implemented on a DS, can be found at `GBATEK
            <https://problemkaputt.de/gbatek.htm#dssoundnotes>`_.

            More information about IMA-ADPCM in general is available at
            `MultimediaWiki
            <https://wiki.multimedia.cx/index.php?title=IMA_ADPCM>`_.


.. py:function:: findInNamedList(L, name)

    Find the value of the item with a particular name in a list containing
    name-value pairs.

    Such a list looks like the following:

    ``[(name1, entry1), (name2, entry2), (name3, entry3), ...]``

    Names are usually :py:class:`str`\s, but not always.

    .. seealso::

        :py:func:`indexInNamedList` -- to retrieve the index of the entry
        instead of its value.

        :py:func:`setInNamedList` -- to replace the value of the entry with a
        new one.

    :param L: The list to search in.

        :type: :py:class:`list` of ``(name, entry)`` where ``name`` is
            typically of type :py:class:`str` and ``entry`` is of any type

    :param name: The name to look for.

        :type: usually :py:class:`str`

    :returns: The value of the list entry with the specified name; that is, the
        second item in that pair.

    :rtype: Whatever type the value in the name-value pair has.

    :raises KeyError: if there is no list item with that name


.. py:function:: indexInNamedList(L, name)

    Find the index of the item with a particular name in a list containing
    name-value pairs.

    Such a list looks like the following:

    ``[(name1, entry1), (name2, entry2), (name3, entry3), ...]``

    Names are usually :py:class:`str`\s, but not always.

    .. seealso::

        :py:func:`findInNamedList` -- to retrieve the value of the entry
        instead of its index.

        :py:func:`setInNamedList` -- to replace the value of the entry with a
        new one.

    :param L: The list to search in.

        :type: :py:class:`list` of ``(name, entry)`` where ``name`` is
            typically of type :py:class:`str` and ``entry`` is of any type

    :param name: The name to look for.

        :type: usually :py:class:`str`

    :returns: The index of the list entry with the specified name.

    :rtype: :py:class:`int`

    :raises KeyError: if there is no list item with that name


.. py:function:: setInNamedList(L, name, value)

    Find the item with a particular name in a list containing name-value pairs,
    and replace its value with a new one. The previous value is discarded.

    Such a list looks like the following:

    ``[(name1, entry1), (name2, entry2), (name3, entry3), ...]``

    Names are usually :py:class:`str`\s, but not always.

    .. seealso::

        :py:func:`findInNamedList` -- to retrieve the value of the entry
        instead of replacing it.

        :py:func:`indexInNamedList` -- to retrieve the index of the entry
        instead of replacing it.

    :param L: The list to search in.

        :type: :py:class:`list` of ``(name, entry)`` where ``name`` is
            typically of type :py:class:`str` and ``entry`` is of any type

    :param name: The name to look for.

        :type: usually :py:class:`str`

    :param value: The new value that the existing value in the list should be
        replaced with.

        :type: Any type.

    :raises KeyError: if there is no list item with that name
