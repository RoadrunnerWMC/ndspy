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

``ndspy.soundGroup``: Sound Groups
==================================

.. module:: ndspy.soundGroup

The ``ndspy.soundGroup`` module  contains classes and enumerations related to
sound groups.

A *group* is a collection of IDs of items that exist elsewhere in an *SDAT*
file, which can be of different types. Games use groups to make lists of files
that should be loaded together.

ndspy represents a group as a :py:class:`list` of :py:class:`GroupEntry`\s.

.. seealso::
    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.


.. py:class:: GroupEntryType

    :base class: :py:class:`enum.IntEnum`

    An enumeration that distinguishes between the types of files that a group
    entry can refer to.

    .. data:: SSEQ

        The group entry refers to a *SSEQ* (sequence) file.

    .. data:: SBNK

        The group entry refers to a *SBNK* (instrument bank) file.

    .. data:: SWAR

        The group entry refers to a *SWAR* (wave archive) file.

    .. data:: SSAR

        The group entry refers to a *SSAR* (sequence archive) file.


.. py:class:: SWARLoadMethod

    :base class: :py:class:`enum.IntEnum`

    An enumeration that distinguishes between the ways in which a *SWAR* can be
    loaded.

    .. note::

        ndspy doesn't expose raw *SDAT* file IDs, and that functionality seems
        to never really be used in practice (and there's honestly no good
        reason to do so), so you don't really need to worry about this very
        much.

    .. data:: FILE_IDS

        :py:attr:`ndspy.soundBank.SBNK.waveArchiveIDs` contains raw *SDAT* file
        IDs.

    .. data:: SWAR_IDs

        :py:attr:`ndspy.soundBank.SBNK.waveArchiveIDs` contains *SWAR* IDs.


.. py:class:: GroupEntry([type[, options[, id]]])

    An entry in a sound group.

    *SSEQ* group entries usually have :py:attr:`GroupEntry.loadSSEQ` and
    :py:attr:`GroupEntry.loadSWAR` set to ``True``, and
    :py:attr:`GroupEntry.SWARLoadMethod` set to
    :py:data:`SWARLoadMethod.SWAR_IDS`.

    *SBNK* group entries usually have :py:attr:`GroupEntry.loadSWAR` set to
    ``True``, and :py:attr:`GroupEntry.SWARLoadMethod` set to
    :py:data:`SWARLoadMethod.SWAR_IDS`.

    *SWAR* group entries usually have :py:attr:`GroupEntry.loadSWAR` set to
    ``True``, and :py:attr:`GroupEntry.SWARLoadMethod` set to
    :py:data:`SWARLoadMethod.SWAR_IDS`.

    *SSAR* group entries usually have :py:attr:`GroupEntry.loadSSAR` set to
    ``True``.

    :param type: The initial value for the :py:attr:`type` attribute.

    :param int options: A bitfield that defines the initial values for
        :py:attr:`loadSSEQ`, :py:attr:`loadSBNKSWARsFrom`, :py:attr:`loadSWAR`,
        and :py:attr:`loadSSAR`.

    :param id: The initial value for the :py:attr:`id` attribute.

    .. py:attribute:: id

        The ID (index) of the file the group entry refers to.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: loadSBNKSWARsFrom

        This attribute determines how *SWAR* IDs in an *SBNK* (see:
        :py:attr:`ndspy.soundBank.SBNK.waveArchiveIDs`) will be interpreted --
        either as raw *SDAT* file IDs or as *SWAR* IDs.

        .. note::

            ndspy doesn't expose raw *SDAT* file IDs, and this functionality
            seems to never really be used in practice (and there's honestly no
            good reason to do so), so you don't really need to worry about this
            very much.

        .. note::
            This value hasn't been tested; the explanation here is based on
            reverse-engineeered code. If you test it, please send a PR to
            update this documentation with your findings!

        :type: :py:class:`SWARLoadMethod`

        :default: :py:data:`SWARLoadMethod.SWAR_IDS`

    .. py:attribute:: loadSSAR

        Whether this group entry should cause a *SSAR* to be loaded.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: loadSSEQ

        Whether this group entry should cause a *SSEQ* to be loaded.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: loadSWAR

        Whether this group entry should cause a *SWAR* to be loaded.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: type

        The type of file the group entry refers to.

        :type: :py:class:`GroupEntryType`

        :default: :py:attr:`GroupEntryType.SSEQ`

    .. py:classmethod:: fromFlags(type, id[, loadSSEQ[, loadSBNKSWARsFrom[, loadSWAR[, loadSSAR]]]])

        Create a sound group entry from individual attribute values.

        :param type: The initial value for the :py:attr:`type` attribute.

        :param id: The initial value for the :py:attr:`id` attribute.

        :param loadSSEQ: The initial value for the :py:attr:`loadSSEQ`
            attribute.

        :param loadSBNKSWARsFrom: The initial value for the
            :py:attr:`loadSBNKSWARsFrom` attribute.

        :param loadSWAR: The initial value for the :py:attr:`loadSWAR`
            attribute.

        :param loadSSAR: The initial value for the :py:attr:`loadSSAR`
            attribute.

        :returns: The sound group entry object.
        :rtype: :py:class:`GroupEntry`

    .. py:function:: save()

        Return this sound group entry's :py:attr:`type`, options value, and
        :py:attr:`id` as a triple. This matches the parameters of the default
        class constructor.

        :returns: The group entry's :py:attr:`type`, options value, and
            :py:attr:`id`.

        :rtype: ``(type, options, id)``, where ``type`` is of type
            :py:class:`GroupEntryType`, ``options`` is of type :py:class:`int`,
            and ``id`` is of type :py:class:`int`
