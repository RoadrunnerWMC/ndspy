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

``ndspy.bmg``: BMG (messages)
=============================

.. py:module:: ndspy.bmg

The ``ndspy.bmg`` module provides support for loading and saving *BMG* files.

*BMG* files contain all of the text in a game that will be displayed to the
player (apart from text embedded into images). Games contain one or more *BMG*
files for each language they support, and will load the appropriate one
depending on the console's language setting. Each "message" is referenced by
index.

Some *BMG* files -- namely, those used in the DS Zelda games -- can contain
scripts that control game progression in addition to text. ndspy can read and
save the file blocks that contain these scripts (*FLW1* and *FLI1*), but
decoding and encoding the instructions themselves is very game-specific and
therefore out of its scope.


.. py:class:: BMG([data], *, [id=0])

    A *BMG* file.

    :param data: The data to be read as a *BMG* file. If this is not provided,
        the *BMG* object will initially be empty.
    :type data: bytes

    :param id: The initial value for the :py:attr:`id` attribute.

    .. py:attribute:: id

        This *BMG*'s ID number. In at least some games, every *BMG* has a
        unique ID. This makes it possible to refer to specific messages by
        specifying the desired *BMG* ID and the message index within that
        *BMG*.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: instructions

        The script instructions in this *BMG*, if it has a *FLW1* block.
        Instructions will be :py:class:`bytes` objects by default, but when
        saving, any object that implements a ``.save() -> bytes`` method is
        acceptable in place of :py:class:`bytes`. (This is to let you implement
        custom classes for instructions if you want to.)

        :type: :py:class:`list` of :py:class:`bytes` or of objects implementing
            ``.save() -> bytes``

        :default: ``[]``

    .. py:attribute:: labels

        The script instruction labels in this *BMG*, if it has a *FLW1* block.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(bmgID, instructionIndex)`` (both
            :py:class:`int`\s)

        :default: ``[]``

    .. py:attribute:: messages

        The list of :py:class:`Message`\s in this *BMG*.

        :type: :py:class:`list` of :py:class:`Message`

        :default: ``[]``

    .. py:attribute:: scripts

        The starting instruction indices for each script ID defined in
        this *BMG*, if it has a *FLI1* block.

        .. seealso::

            :py:func:`ndspy.indexInNamedList`,
            :py:func:`ndspy.findInNamedList`,
            :py:func:`ndspy.setInNamedList` -- helper functions you can use to
            find and replace values in this list.

        :type: :py:class:`list` of ``(scriptID, instructionIndex)`` (both
            :py:class:`int`\s)

        :default: ``[]``

    .. py:attribute:: unk10

        Unknown header value at 0x10.

        :type: :py:class:`int`

        :default: 2

    .. py:attribute:: unk14

        Unknown header value at 0x14.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk18

        Unknown header value at 0x18.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: unk1C

        Unknown header value at 0x1C.

        :type: :py:class:`int`

        :default: 0

    .. py:classmethod:: fromMessages(messages, [instructions, [labels, [scripts]]], *, [id=0])

        Create a *BMG* from a list of messages.

        :param messages: The initial value for the :py:attr:`messages`
            attribute.

        :param instructions: The initial value for the :py:attr:`instructions`
            attribute.

        :param labels: The initial value for the :py:attr:`labels` attribute.

        :param scripts: The initial value for the :py:attr:`scripts` attribute.

        :param id: The initial value for the :py:attr:`id` attribute.

        :returns: The *BMG* object.
        :rtype: :py:class:`BMG`

    .. py:classmethod:: fromFile(filePath[, ...])

        Load a *BMG* from a filesystem file. This is a convenience function.

        :param filePath: The path to the *BMG* file to open.
        :type filePath: :py:class:`str` or other path-like object

        Further parameters are the same as those of the default constructor.

        :returns: The *BMG* object.
        :rtype: :py:class:`BMG`

    .. py:function:: save()

        Generate file data representing this *BMG*.

        *FLW1* and *FLI1* sections will be created only if any script
        instructions or scripts exist, respectively.

        :returns: The *BMG* file data.
        :rtype: :py:class:`bytes`

    .. py:function:: saveToFile(filePath)

        Generate file data representing this *BMG*, and save it to a filesystem
        file. This is a convenience function.

        *FLW1* and *FLI1* sections will be created only if any script
        instructions or scripts exist, respectively.

        :param filePath: The path to the *BMG* file to save to.
        :type filePath: :py:class:`str` or other path-like object


.. py:class:: Message([info[, stringParts[, isNull]]])

    A single message in a *BMG* file.

    *BMG* messages are more than simple strings; they contain escape sequences
    that can specify font formatting and allow text to be inserted at runtime.
    For this reason, the message data is represented as a list of strings and
    :py:class:`Escape`\s instead of as a string.

    :param info: The initial value for the :py:attr:`info` attribute.

    :param stringParts: The initial value of the :py:attr:`stringParts`
        attribute.

    :param isNull: The initial value for the :py:attr:`isNull` attribute.

    .. py:attribute:: info

        A value representing message metadata, which comes from the *BMG*'s
        *INF1* block. The specific meaning of this value is currently unclear.

        :type: :py:class:`int`

        :default: 0

    .. py:attribute:: isNull

        This is ``True`` if the message is null; that is, if its data offset
        value in *INF1* is 0.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: stringParts

        A list of strings and escape sequences that together form the message.
        Empty strings are allowed but discouraged.

        :type: :py:class:`list` of :py:class:`str` and of :py:class:`Escape`

        :default: ``[]``

    .. py:function:: save()

        Generate binary data representing this message.

        :returns: The message data.
        :rtype: :py:class:`bytes`


.. py:class:: Message.Escape([type[, data]])

    An escape sequence within a *BMG* message.

    Escape sequences have a type and optional parameter data. Currently, the
    parameter data is left raw and unparsed; this may change in the future.

    :param type: The initial value for the :py:attr:`type` attribute.

    :param data: The initial value of the :py:attr:`data` attribute.

    .. py:attribute:: data

        The raw data contained in this escape sequence.

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: type

        The type ID of this escape sequence.

        :type: :py:class:`int`

        :default: 0

    .. py:function:: save()

        Generate binary data representing this escape sequence.

        :returns: The escape sequence data.
        :rtype: :py:class:`bytes`
