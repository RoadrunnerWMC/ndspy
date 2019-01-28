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


.. py:class:: NARC([data])

    A *NARC* archive file.

    :param data: The data to be read as a *NARC* file. If this is not provided,
        the *NARC* object will initially be empty.
    :type data: bytes

    .. py:attribute:: endiannessOfBeginning

        The endianness of the first 8 bytes of the *NARC* file header. The rest
        of the file is always little-endian.

        ``'<'`` and ``'>'`` (representing little-endian and big-endian,
        respectively) are the only values this attribute is allowed to take.

        :type: :py:class:`str`

        :default: ``'<'``

    .. py:attribute:: filenames

        The root folder of the *NARC*'s filename table.

        .. seealso::

            :py:mod:`ndspy.fnt` -- the ndspy module the
            :py:class:`ndspy.fnt.Folder` class resides in.

            :py:attr:`files` -- the corresponding list of files that these
            filenames refer to.

        :type: :py:class:`ndspy.fnt.Folder`

        :default: ``ndspy.fnt.Folder()``

    .. py:attribute:: files

        The list of files in this *NARC*. Indices are file IDs; that is,
        ":py:attr:`files`\[0]" is the file with file ID 0,
        ":py:attr:`files`\[1]" is the file with file ID 1, etc.

        .. seealso::

            :py:attr:`filenames` -- the set of filenames for these files.

        :type: :py:class:`list` of :py:class:`bytes`

        :default: ``[]``

    .. py:classmethod:: fromFilesAndNames(files[, filenames])

        Create a *NARC* archive from a list of files and (optionally) a
        filename table.

        :param files: The initial value for the :py:attr:`files` attribute.

        :param filenames: The initial value for the :py:attr:`filenames`
            attribute.

        :returns: The *NARC* object.
        :rtype: :py:class:`NARC`

    .. py:classmethod:: fromFile(filePath)

        Load a *NARC* archive from a filesystem file. This is a convenience
        function.

        :param filePath: The path to the *NARC* file to open.
        :type filePath: :py:class:`str` or other path-like object

        :returns: The *NARC* object.
        :rtype: :py:class:`NARC`

    .. py:function:: getFileByName(filename)

        Return the data for the file with the given filename (path). This is a
        convenience function; the following two lines of code are exactly
        equivalent (apart from some error checking):

        .. code-block:: python

            fileData = narc.getFileByName(filename)
            fileData = narc.files[narc.filenames.idOf(filename)]

        .. seealso::
            :py:func:`setFileByName` -- to replace the file data instead of
            retrieving it.

        :param str filename: The name of the file.

        :returns: The file's data.
        :rtype: :py:class:`bytes`

    .. py:function:: setFileByName(filename, data)

        Replace the data for the file with the given filename (path) with the
        given data. This is a convenience function; the following two lines of
        code are exactly equivalent (apart from some error checking):

        .. code-block:: python

            narc.setFileByName(filename, fileData)
            narc.files[narc.filenames.idOf(filename)] = fileData

        .. seealso::
            :py:func:`getFileByName` -- to retrieve the file data
            instead of replacing it.

        :param str filename: The name of the file.
        :param bytes data: The new data for the file.

    .. py:function:: save()

        Generate file data representing this *NARC*.

        :returns: The *NARC* archive file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *NARC*, and save it to a
        filesystem file. This is a convenience function.

        :param filePath: The path to the *NARC* archive file to save to.
        :type filePath: :py:class:`str` or other path-like object
