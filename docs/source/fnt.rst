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

``ndspy.fnt``: Filename Tables
==============================

.. py:module:: ndspy.fnt

ROM files (:py:mod:`ndspy.rom`) and NARC archives (:py:mod:`ndspy.narc`) both
use the same format for filename tables. ``ndspy.fnt`` provides a consistent
interface for these.

.. warning::

    Some games (such as *New Super Mario Bros.*) load files by hardcoded file
    IDs rather than by their filenames. Thus, when editing filename tables, you
    should avoid changing existing file IDs unless you're sure that the game
    loads files by their filenames.

A filename table is represented as a :py:class:`Folder`. This class does not
contain any file data; it merely defines the folder hierarchy, and names of
folders and files. As such, this particular page of documentation page will use
the terms "filename" and "file" rather interchangeably.


.. _file-names-and-file-ids:

Filenames and file IDs
----------------------

It's important to understand how file IDs relate to filenames. Here's an
example directory structure showing both filenames and file IDs:

.. code-block:: none

    (root)/                             87
        barrier-skip.mp4                (87)
        sm64-upwarp.zip                 (88)
        books/                          89
            hyrule-historia.pdf         (89)
            ndspy-documentation.pdf     (90)
            lord-of-the-rings/          91
                book1.pdf               (91)
                book2.pdf               (92)
                book3.pdf               (93)
        songs/                          94
            smb3-athletic.mp3           (94)
            zeldas-lullaby.mp3          (95)

Folders have a "first ID" attribute (:py:attr:`Folder.firstID`) that specifies
the ID of the first file within the folder; these are shown above as numbers
without parentheses. The files within the folder then implicitly have ascending
file IDs starting with that value; these are shown above as parenthesized
numbers.

Files in a folder's subfolders have IDs greater than those of the files
directly in the folder. Files and folders are usually sorted in ASCIIbetical
order, though that probably does not have to be the case.

File IDs referenced by a filename table do not always start at 0. ROMs, for
instance, usually include overlays as unnamed files starting at ID 0, causing
the filename table to begin at some higher file ID.


.. py:function:: load(fnt)

    Create a :py:class:`Folder` from filename table data. This is the
    inverse of :py:func:`save`.

    :param bytes fnt: The filename table data to parse.

    :returns: The root folder of the filename table.
    :rtype: :py:class:`Folder`


.. py:function:: save(root)

    Generate a :py:class:`bytes` object representing this root folder as
    a filename table. This is the inverse of :py:func:`load`.

    :param Folder root: The root folder of the filename table.

    :returns: The filename table data.
    :rtype: :py:class:`bytes`


.. py:class:: Folder([folders[, files[, firstID]]])

    A single folder within a filename table, or an entire filename table --
    ndspy does not make a distinction between these. It can contain subfolders
    (:py:attr:`folders`) and files (:py:attr:`files`).

    All files within a folder implicitly have consecutive IDs. This is done by
    only specifying the ID of the first file in the folder
    (:py:attr:`firstID`). The second file in the folder then has file ID
    ":py:attr:`firstID` + 1", the third has ":py:attr:`firstID` + 2", etc. See
    the introduction to this page for a more thorough explanation.

    :param folders: The initial value for the :py:attr:`folders` attribute.

    :param files: The initial value for the :py:attr:`files` attribute.

    :param firstID: The initial value for the :py:attr:`firstID` attribute.

    .. note::

        For convenience, :py:class:`Folder` supports indexing syntax
        (``folder[key]``):

        *   If the key is a :py:class:`int`, indexing is equivalent to calling
            :py:func:`filenameOf`.

        *   If the key is a :py:class:`str`, indexing is equivalent to first
            calling :py:func:`idOf`, and then calling :py:func:`subfolder` if
            that returns ``None``.

        Thus, you can index by file ID to retrieve a filename, index by
        filename to get a file ID, and index by subfolder name to get a
        :py:class:`Folder` instance.

        .. warning::
            Unless you know exactly what the filename table you're parsing
            contains, it's a good idea to explicitly use :py:func:`idOf` and
            :py:func:`subfolder` instead of indexing syntax for retrieving file
            IDs. Indexing syntax is the same for accessing both files and
            subfolders, so you may run into confusing problems if a subfolder
            with the same name as the file you're looking for exists, or vice
            versa.

        :raises TypeError: if a folder is indexed by something other than a
            :py:class:`str` or :py:class:`int`

        :raises KeyError: if the given file ID or filename or subfolder name
            cannot be found

    .. py:attribute:: files

        The files within this folder. The first one implicitly has file ID
        :py:attr:`firstID`, the second has file ID ":py:attr:`firstID` + 1",
        and so on.

        :type: :py:class:`list` of :py:class:`str`

        :default: ``[]``

    .. py:attribute:: firstID

        The file ID of the first file within this folder (that is, the file ID
        of ":py:attr:`files`\[0]").

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: folders

        The folders contained within this folder.

        This is presented as a list of name-value pairs because
        :py:class:`collections.OrderedDict` -- the best choice for an
        order-preserving dictionary type -- does not provide an easy way to
        adjust the order of its elements.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(name, folder)``, where ``name`` is of
            type :py:class:`str` and ``folder`` is of type :py:class:`Folder`

        :default: ``[]``

    .. py:function:: idOf(path)

        Find the file ID for the given filename, or for the given file path
        (using ``/`` as the separator) relative to this folder.

        .. seealso::

            :py:func:`subfolder`
                The equivalent function for finding folders instead of files.

        :param str path: The filename or ``/``-separated file path to look for.

        :returns: The file ID, or ``None`` if no such file is found.
        :rtype: :py:class:`int` or ``None``

    .. py:function:: filenameOf(id)

        Find the filename of the file with the given ID. If it exists in a
        subfolder, the filename will be returned as a path separated by
        forward slashes (``/``).

        :param int id: The file ID to look for.

        :returns: The filename, or ``None`` if no file with that ID exists or
            if the file has no name.
        :rtype: :py:class:`str` or ``None``

    .. py:function:: subfolder(path)

        Find the :py:class:`Folder` instance for the given subfolder name, or
        for the given folder path (using ``/`` as the separator) relative to
        this folder.

        .. seealso::

            :py:func:`idOf`
                The equivalent function for finding files instead of folders.

        :param str path: The subfolder name or ``/``-separated folder path to
            look for.

        :returns: The folder, or ``None`` if no such folder is found.
        :rtype: :py:class:`Folder` or ``None``
