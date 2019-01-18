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

``ndspy.soundWaveArchive``: Sound Wave Archives
===============================================

.. module:: ndspy.soundWaveArchive

The ``ndspy.soundWaveArchive`` module lets you edit and create *SWAR* files,
which are essentially just slightly glorified lists of *SWAV* files.

.. seealso::

    If you aren't familiar with how *SDAT* files are structured, consider
    reading :doc:`the appendix explaining this <sdatStructure>`.

    Documentation about the *SWAV* files within *SWAR*\s can be found on the
    :doc:`soundWave` page.


.. py:class:: SWAR([file[, unk02]])

    A *SWAR* sound wave archive.

    :param bytes file: The data to be read as a *SWAR* file. If this is not
        provided, the *SWAR* object will initially be empty.

    :param unk02: The initial value for the :py:attr:`unk02` attribute.

    .. py:attribute:: dataMergeOptimizationID

        When saving a *SDAT* file containing multiple *SWAR* files, ndspy will
        check if any of them save to identical data. If it finds any, it will
        only encode the data for them once and then reference it multiple
        times, to save some space. This attribute is an extra field that is
        also compared between *SWAR* files, which you can use to exclude
        particular ones from this optimization.

        Since this defaults to 0 for all *SWAR*\s created from scratch, this
        optimization will happen by default. It's unlikely that you will need
        to use this attribute to disable the optimization, but you can.

        .. note::

            This value is not explicitly saved in the *SWAR* file or in the
            *SDAT* file containing it.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk02

        The value following the *SWAR*'s file ID in the "INFO" section of the
        *SDAT* file it is contained in. Its purpose is unknown.

        .. note::

            This value is not explicitly saved in the *SWAR* file, but it is
            saved in the *SDAT* file if the *SWAR* is within one.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: waves

        The *SWAV* objects contained in this *SWAR*. "Wave IDs" or "SWAV IDs"
        are simply indices into this list.

        :type: :py:class:`list` of :py:class:`ndspy.soundWave.SWAV`

        :default: ``[]``

    .. py:classmethod:: fromWaves(waves[, unk02])

        Create a *SWAR* from a list of *SWAV*\s.

        :param waves: The initial value for the :py:attr:`waves` attribute.

        :param unk02: The initial value for the :py:attr:`unk02` attribute.

        :returns: The *SWAR* object.
        :rtype: :py:class:`SWAR`

    .. py:classmethod:: fromFile(filePath[, unk02])

        Load a *SWAR* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *SWAR* file to open.
        :type filePath: :py:class:`str` or other path-like object

        :param unk02: The initial value for the :py:attr:`unk02` attribute.

        :returns: The *SWAR* object.
        :rtype: :py:class:`SWAR`

    .. py:function:: save()

        Generate file data representing this *SWAR*, and then return that data
        and :py:attr:`unk02` as a pair (2-tuple). This matches the parameters
        of the default class constructor.

        :returns: The *SWAR* file data and :py:attr:`unk02`.

        :rtype: ``(data, unk02)``, where ``data`` is of type :py:class:`bytes`
            and ``unk02`` is of type :py:class:`int`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *SWAR*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *SWAR* file to save to.
        :type filePath: :py:class:`str` or other path-like object
