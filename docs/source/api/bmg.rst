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

In games that use them, *BMG* files generally contain most or all of the text
that can be displayed to the player (apart from text embedded into images).
Games contain one or more *BMG* files for each language they support, and will
load the appropriate one depending on the console's language setting. Each
"message" is referenced by index.

Some *BMG* files -- namely, those used in the DS Zelda games -- can contain
scripts that control game progression in addition to text. ndspy can read and
save the file blocks that contain these scripts (*FLW1* and *FLI1*), but
decoding and encoding the instructions themselves is very game-specific and
therefore out of its scope.


Examples
--------

Load a *BMG* from a ROM and inspect its messages and scripts:

.. code-block:: python

    >>> import ndspy.rom, ndspy.bmg
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('Zelda - Spirit Tracks.nds')
    >>> bmgData = rom.getFileByName('English/Message/castle_town.bmg')
    >>> bmg = ndspy.bmg.BMG(bmgData)
    >>> print(bmg)
    <bmg id=12 (159 messages, 26 scripts)>
    >>> print(bmg.messages[2])
    What took you so long,
    [254:0000]?

    Did you keep me waiting
    just so you could change
    clothes?
    >>> bmg.messages[2].stringParts
    ['What took you so long,\n', Escape(254, bytearray(b'\x00\x00')), '?\n\nDid you keep me waiting\njust so you could change\nclothes?']
    >>> bmg.scripts[:5]
    [(6553601, 9), (6553602, 140), (6553604, 117), (6553605, 124), (6553609, 183)]
    >>> bmg.labels[:5]
    [(12, 28), (-1, -1), (12, 0), (12, 68), (12, 73)]
    >>> bmg.instructions[:5]
    [bytearray(b'\x033\x00\x00e\x00\x00\x00'), bytearray(b'\x03\n\x01\x00\n\x00\r\x00'), bytearray(b'\x033\x02\x00\x03\x00\x00\x00'), bytearray(b'\x033\x03\x00\x02\x00\x00\x00'), bytearray(b'\x033\x04\x00\x04\x00\x00\x00')]
    >>>

Load a *BMG* from a file, edit a message, and save it back into a ROM:

.. code-block:: python

    >>> import ndspy.bmg, ndspy.rom
    >>> bmg = ndspy.bmg.BMG.fromFile('course.bmg')
    >>> print(bmg.messages[15])
    Welcome to the secret
    Challenge mode. Think you can
    reach the goal? If you get
    stuck, press START and choose
    Return to Map.
    >>> bmg.messages[15].stringParts = ["Welcome to the secret\nChallenge mode where it's\nvery easy to softlock."]
    >>> print(bmg.messages[15])
    Welcome to the secret
    Challenge mode where it's
    very easy to softlock.
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')
    >>> rom.setFileByName('script/course.bmg', bmg.save())
    >>> rom.saveToFile('nsmb_edited.nds')
    >>>

Create a new *BMG* using the ``cp1252`` encoding, and save it to a file:

.. code-block:: python

    >>> import ndspy.bmg
    >>> message1 = ndspy.bmg.Message(b'', ['Want to save your game?'])
    >>> message2 = ndspy.bmg.Message(b'', ["Sure!\nNo thanks."])
    >>> bmg = ndspy.bmg.BMG.fromMessages([message1, message2])
    >>> bmg.encoding = 'cp1252'
    >>> bmg.saveToFile('savegame-en-us.bmg')
    >>>


API
---

.. py:class:: BMG([data], *, [id=0])

    A *BMG* file.

    :param data: The data to be read as a *BMG* file. If this is not provided,
        the *BMG* object will initially be empty.
    :type data: bytes

    :param id: The initial value for the :py:attr:`id` attribute. The *BMG*
        data itself might optionally specify its own ID; if it does, that value
        takes precedence and this parameter is ignored.

    .. py:attribute:: encoding

        The encoding that should be used for storing strings in the *BMG*.
        Choosing an encoding is a trade-off between space efficiency, time
        efficiency, and the amount and choice of characters that can be
        encoded.

        Valid encodings are ``cp1252``, ``utf-16``, ``shift-jis``, and
        ``utf-8``.

        .. seealso::

            :attr:`fullEncoding` -- a read-only mirror of this property that
            includes endianness information, intended for use with
            ``str.encode()`` and ``bytes.decode()``.

        :type: :py:class:`str`

        :default: ``'utf-16'``

    .. py:attribute:: fullEncoding

        A mirror property for :attr:`encoding` that takes :attr:`endianness`
        into account. This can be used with ``str.encode()`` or
        ``bytes.decode()``, if for some reason you need to encode or decode raw
        string data matching this *BMG*'s encoding.

        The value of this attribute will always be the same as that of
        :attr:`encoding`, unless that attribute has the value ``utf-16``. In
        that case, this property will be either ``utf-16le`` or ``utf-16be``,
        depending on :attr:`endianness`.

        This attribute is read-only.

        .. seealso::

            :attr:`encoding` -- a writable property you can use to modify the
            *BMG*'s encoding.

        :type: :py:class:`str`

        :default: ``'utf-16le'``

    .. py:attribute:: endianness

        Whether values in the *BMG* should be stored using big- or
        little-endian byte order. Since the Nintendo DS is by default a
        little-endian console, almost every game uses little-endian *BMG*
        files. An exception to this is *Super Princess Peach.*

        ``'<'`` and ``'>'`` (representing little-endian and big-endian,
        respectively) are the only values this attribute is allowed to take.

        :type: :py:class:`str`

        :default: ``'<'``

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
        attribute. If you pass a bare string for this parameter, it will be
        automatically wrapped in a list for you.

    :param isNull: The initial value for the :py:attr:`isNull` attribute.

    .. py:attribute:: info

        A value containing message metadata, which comes from the *BMG*'s
        *INF1* block.

        The meaning of this value is completely game-dependent, and some games
        just leave this empty and don't use it at all.

        .. warning::

            While the amount of metadata per message varies from game to game,
            it's always required that all messages in a *BMG* have the same
            amount of metadata. If you violate this, you'll experience errors
            when trying to save!

        :type: :py:class:`bytes`

        :default: ``b''``

    .. py:attribute:: isNull

        This is ``True`` if the message is null; that is, if its data offset
        value in *INF1* is 0. A null message should have an empty
        :py:attr:`stringParts` list.

        .. note::

            :py:class:`Message`\s with this attribute set to ``True`` are used
            to represent empty messages instead of ``None`` because empty
            messages can still have non-empty :py:attr:`info` values.

        :type: :py:class:`bool`

        :default: ``False``

    .. py:attribute:: stringParts

        A list of strings and escape sequences that together form the message.
        Empty strings are allowed but discouraged.

        :type: :py:class:`list` of :py:class:`str` and of :py:class:`Escape`

        :default: ``[]``

    .. py:function:: save(encoding)

        Generate binary data representing this message.

        :param str encoding: The encoding to use for the string data in the
            message (i.e. ``'utf-16'``, ``'ascii'``, etc).

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

    .. py:function:: save(encoding)

        Generate binary data representing this escape sequence.

        :param str encoding: The encoding that should be assumed when building
            the binary data for the escape sequence (i.e. ``'utf-16'``,
            ``'ascii'``, etc). This is used to properly encode the escape
            character itself, U+001A.

        :returns: The escape sequence data.
        :rtype: :py:class:`bytes`
