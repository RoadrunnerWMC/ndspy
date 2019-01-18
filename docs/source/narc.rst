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

``ndspy.narc``: NARC Archives
=============================

.. py:module:: ndspy.narc

The ``ndspy.narc`` module allows you to open and save *NARC* archive files.

*NARC* archives are structured similarly to ROM files, in that each file can be
referenced by either ID or by a filename from a filename table. Filename tables
work the same as those of ROMs.


.. py:function:: load(data)

    Read *NARC* data, and create a filename table and a list of files. This is
    the inverse of :py:func:`save`.

    :param bytes data: The *NARC* archive file data.

    :returns: The root folder of the filename table, and a list of files as
        :py:class:`bytes`.

    :rtype: ``(folder, files)``, where ``folder`` is of type
        :py:class:`ndspy.fnt.Folder` and ``files`` is a :py:class:`list` of
        :py:class:`bytes`


.. py:function:: loadFromFile(filePath)

    Load a *NARC* archive from a filesystem file, and create a filename table
    and a list of files. This is the inverse of :py:func:`saveToFile`.

    :param filePath: The path to the *NARC* archive file to open.
    :type filePath: :py:class:`str` or other path-like object

    :returns: The root folder of the filename table, and a list of files as
        :py:class:`bytes`.

    :rtype: ``(folder, files)``, where ``folder`` is of type
        :py:class:`ndspy.fnt.Folder` and ``files`` is a :py:class:`list` of
        :py:class:`bytes`


.. py:function:: save(filenames, fileList)

    Create a *NARC* archive from a filename table and a list of files. This is
    the inverse of :py:func:`load`.

    :param Folder filenames: The root folder of the filename table.

    :param fileList: The list of files to include in the archive.
    :type fileList: :py:class:`list` of :py:class:`bytes`

    :returns: The *NARC* archive.

    :rtype: :py:class:`bytes`


.. py:function:: saveToFile(filenames, fileList, filePath)

    Create a *NARC* archive from a filename table and a list of files, and
    save it to a filesystem file. This is the inverse of
    :py:func:`loadFromFile`.

    :param Folder filenames: The root folder of the filename table.

    :param fileList: The list of files to include in the archive.
    :type fileList: :py:class:`list` of :py:class:`bytes`

    :param filePath: The path to the *NARC* archive file to save to.
    :type filePath: :py:class:`str` or other path-like object
