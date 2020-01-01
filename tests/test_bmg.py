# Copyright 2019 RoadrunnerWMC
#
# This file is part of ndspy.
#
# ndspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ndspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ndspy.  If not, see <https://www.gnu.org/licenses/>.
"""
Unit tests for ndspy.bmg.
"""


import pathlib
import struct

import ndspy.bmg
import pytest


FILES_PATH = pathlib.Path('../test_files/bmg')


# Some example values to use in various contexts

STRINGS = ['Hello world',
           'Lorem ipsum dolor sit amet',
           'ABCDEFG',
           '\nHIJK\nLMNOP\n']
MESSAGES = [ndspy.bmg.Message(b'', s) for s in STRINGS]

MESSAGE_INFOS = [b'\0\1\2', b'\3\4\5', b'\6\7\x08', b'\xFD\xFE\xFF']

INSTRUCTIONS = [bytes.fromhex('fa90a01bc0b92da9'),
                bytes.fromhex('627edff30d866102'),
                bytes.fromhex('2074f5830d26ad1b'),
                bytes.fromhex('130976e27107edcf'),
                bytes.fromhex('85989970bed149aa')]

# TODO: why are label values signed, exactly? Is that a mistake?
# TODO: why is label (0, 0) in particular ignored during loading?
LABELS = [(1, 2),
          (3, 4),
          (0x7E, 0x7C7D),
          (0x7F, 0x7E7F),
          (-1, -1),
          (-0x80, -0x8000)]

SCRIPTS = [(0, 0),
           (1, 2),
           (3, 4),
           (0xF8F9FAFB, 0xFCFD),
           (0xFCFDFEFF, 0xFEFF)]

MESSAGE_PARTS = list(STRINGS)
MESSAGE_PARTS.insert(1, ndspy.bmg.Message.Escape(7, b'abcdefg'))
MESSAGE_PARTS.insert(3, ndspy.bmg.Message.Escape(0, b''))
MESSAGE_PARTS.insert(5, ndspy.bmg.Message.Escape(0xFF, b'hijk'))


def test_empty():
    """
    Test loading an empty BMG
    """
    data = (FILES_PATH / 'empty.bmg').read_bytes()
    bmg = ndspy.bmg.BMG(data)

    assert bmg.encoding == 'utf-16'
    assert bmg.endianness == '<'
    assert bmg.id == 0
    assert bmg.instructions == []
    assert bmg.labels == []
    assert bmg.messages == []
    assert bmg.scripts == []
    assert bmg.unk14 == 0
    assert bmg.unk18 == 0
    assert bmg.unk1C == 0

    assert bmg.save() == data


def test_encoding():
    """
    Test all supported encodings
    """
    # Available encodings and their IDs
    ENCODINGS = {
        'cp1252': 1,
        'utf-16': 2,
        'shift-jis': 3,
        'utf-8': 4,
    }

    # Ensure it raises exceptions for unknown/invalid encodings
    bmg = ndspy.bmg.BMG()
    bmg.encoding = None
    with pytest.raises(ValueError):
        bmg.save()
    bmg.encoding = 'sfgkjhsdghkjdhfg'
    with pytest.raises(ValueError):
        bmg.save()

    def testLoad(encoding, messages, data, endianness='<'):
        """
        Load a BMG from the provided data, and ensure it uses the
        requested encoding and that the messages match the specified
        list of strings.
        """
        assert data[0x10] == ENCODINGS[encoding]

        bmg = ndspy.bmg.BMG(data)

        assert bmg.encoding == encoding
        assert bmg.endianness == endianness

        assert len(bmg.messages) == len(messages)
        for message, s in zip(bmg.messages, messages):
            assert message.stringParts == [s]

    def testSave(encoding, messages, data, endianness='<'):
        """
        Save a BMG with the given encoding and messages, and ensure the
        data matches the provided data.
        """
        bmg = ndspy.bmg.BMG.fromMessages(
            [ndspy.bmg.Message(b'', s) for s in messages])
        bmg.encoding = encoding
        bmg.endianness = endianness

        new_data = bmg.save()
        assert new_data == data
        assert new_data[0x10] == ENCODINGS[encoding]

    def testUnsaveable(encoding, messages):
        """
        Assert that the provided messages cannot be encoded in the given
        encoding.
        """
        bmg = ndspy.bmg.BMG.fromMessages(
            [ndspy.bmg.Message(b'', s) for s in messages])
        bmg.encoding = encoding

        with pytest.raises(Exception):
            bmg.save()

    # Basic test that exercises all codepoints between 01 and 7F,
    # excluding 1A. Should be compatible with every encoding.
    messages = [bytes([*range(1, 0x1A), *range(0x1B, 0x80)]).decode('cp1252')]
    data = (FILES_PATH / '01-19_1B-7F_cp1252.bmg').read_bytes()
    testLoad('cp1252', messages, data)
    testSave('cp1252', messages, data)
    data = (FILES_PATH / '01-19_1B-7F_utf-16le.bmg').read_bytes()
    testLoad('utf-16', messages, data)
    testSave('utf-16', messages, data)
    data = (FILES_PATH / '01-19_1B-7F_utf-16be.bmg').read_bytes()
    testLoad('utf-16', messages, data, '>')
    testSave('utf-16', messages, data, '>')
    data = (FILES_PATH / '01-19_1B-7F_shift-jis.bmg').read_bytes()
    testLoad('shift-jis', messages, data)
    testSave('shift-jis', messages, data)
    data = (FILES_PATH / '01-19_1B-7F_utf-8.bmg').read_bytes()
    testLoad('utf-8', messages, data)
    testSave('utf-8', messages, data)

    # Test codepoints 80-FF. Should be compatible with all except CP1252
    # and Shift-JIS.
    messages = [bytes(range(0x80, 0x100)).decode('latin-1')]
    testUnsaveable('cp1252', messages)
    data = (FILES_PATH / '80-FF_utf-16le.bmg').read_bytes()
    testLoad('utf-16', messages, data)
    testSave('utf-16', messages, data)
    data = (FILES_PATH / '80-FF_utf-16be.bmg').read_bytes()
    testLoad('utf-16', messages, data, '>')
    testSave('utf-16', messages, data, '>')
    testUnsaveable('shift-jis', messages)
    data = (FILES_PATH / '80-FF_utf-8.bmg').read_bytes()
    testLoad('utf-8', messages, data)
    testSave('utf-8', messages, data)

    # Bytes A1-DF, though, *should* be compatible with CP1252 and
    # Shift-JIS.
    messages = [bytes(range(0xA1, 0xDF)).decode('cp1252')]
    data = (FILES_PATH / 'A1-DF_cp1252.bmg').read_bytes()
    testLoad('cp1252', messages, data)
    testSave('cp1252', messages, data)
    messages = [bytes(range(0xA1, 0xDF)).decode('shift-jis')]
    data = (FILES_PATH / 'A1-DF_shift-jis.bmg').read_bytes()
    testLoad('shift-jis', messages, data)
    testSave('shift-jis', messages, data)


def test_fullEncoding():
    """
    Test the BMG.fullEncoding attribute.
    """
    bmg = ndspy.bmg.BMG()

    bmg.endianness = '<'
    bmg.encoding = 'cp1252'; assert bmg.fullEncoding == 'cp1252'
    bmg.encoding = 'utf-16'; assert bmg.fullEncoding == 'utf-16le'
    bmg.encoding = 'shift-jis'; assert bmg.fullEncoding == 'shift-jis'
    bmg.encoding = 'utf-8'; assert bmg.fullEncoding == 'utf-8'

    bmg.endianness = '>'
    bmg.encoding = 'cp1252'; assert bmg.fullEncoding == 'cp1252'
    bmg.encoding = 'utf-16'; assert bmg.fullEncoding == 'utf-16be'
    bmg.encoding = 'shift-jis'; assert bmg.fullEncoding == 'shift-jis'
    bmg.encoding = 'utf-8'; assert bmg.fullEncoding == 'utf-8'


def test_badCharDetection():
    """
    Test detecting illegal characters in message strings (00 and 1A)
    """
    bmg = ndspy.bmg.BMG()

    for bad in '\x00\x1A':
        bmg.messages = [ndspy.bmg.Message(b'', f'hello {bad} world')]

        for encoding in ['cp1252', 'utf-16', 'shift-jis', 'utf-8']:
            bmg.encoding = encoding

            with pytest.raises(ValueError):
                bmg.save()


def test_endianness():
    """
    Test the BMG.endianness attribute
    """
    # We'll use the file-length attribute to manually check endianness,
    # like the bmg module does. (That shouldn't cause any problems.)

    # For both endiannesses, check that the ID value is properly loaded
    data = (FILES_PATH / 'endian_le.bmg').read_bytes()
    assert data[0x08:0x0C] == struct.pack('<I', len(data))
    bmg = ndspy.bmg.BMG(data)
    assert bmg.endianness == '<'
    assert bmg.id == 0x12345678

    data = (FILES_PATH / 'endian_be.bmg').read_bytes()
    assert data[0x08:0x0C] == struct.pack('>I', len(data))
    bmg = ndspy.bmg.BMG(data)
    assert bmg.endianness == '>'
    assert bmg.id == 0x12345678

    # Now check stuff for a from-scratch BMG...
    bmg = ndspy.bmg.BMG()

    # Default endianness should be LE
    assert bmg.endianness == '<'
    # Check that it saves as expected
    data = bmg.save()
    assert data[0x08:0x0C] == struct.pack('<I', len(data))
    # Switcch to BE and check that as well
    bmg.endianness = '>'
    data = bmg.save()
    assert data[0x08:0x0C] == struct.pack('>I', len(data))


def test_id():
    """
    Test BMG IDs
    """

    # Check that a nonzero ID is loaded (regardless of endianness)
    bmg = ndspy.bmg.BMG.fromFile(FILES_PATH / 'id.bmg')
    assert bmg.endianness == '<'
    assert bmg.id == 0x12345678

    # And check that it's saved to the right place
    assert ndspy.bmg.BMG(id=0x12345678).save()[0x2C:0x30] == b'\x78\x56\x34\x12'

    # empty.bmg specifies an ID of 0, which should take precedence over
    # the "id" constructor parameter
    data = (FILES_PATH / 'empty.bmg').read_bytes()
    assert ndspy.bmg.BMG(data).id == 0
    assert ndspy.bmg.BMG(data, id=7).id == 0

    # (Same as above but with the .fromFile() constructor)
    assert ndspy.bmg.BMG.fromFile(FILES_PATH / 'empty.bmg').id == 0
    assert ndspy.bmg.BMG.fromFile(FILES_PATH / 'empty.bmg', id=7).id == 0

    # However, if we load a BMG lacking an INF1 block, then the id
    # parameter should be respected
    data = (FILES_PATH / 'no_inf1.bmg').read_bytes()
    assert ndspy.bmg.BMG(data, id=7).id == 7
    assert ndspy.bmg.BMG(data, id=8).id == 8

    # (Same as above but with the .fromFile() constructor)
    assert ndspy.bmg.BMG.fromFile(FILES_PATH / 'no_inf1.bmg', id=7).id == 7
    assert ndspy.bmg.BMG.fromFile(FILES_PATH / 'no_inf1.bmg', id=8).id == 8


def test_instructions():
    """
    Test the BMG.instructions attribute
    """

    # Try loading a BMG containing example instructions
    data = (FILES_PATH / 'instructions.bmg').read_bytes()
    assert ndspy.bmg.BMG(data).instructions == INSTRUCTIONS

    # Make a new BMG with the same instructions and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.instructions = INSTRUCTIONS
    assert new_bmg.save() == data

    # Define an "Instruction" class with a save() method, which should
    # be acceptable in place of bytes objects
    class Instruction:
        def __init__(self, value):
            self.value = value
        def save(self):
            return self.value

    # Ensure that Instruction objects can indeed be used like that
    new_bmg = ndspy.bmg.BMG()
    new_bmg.instructions = [Instruction(v) for v in INSTRUCTIONS]
    assert new_bmg.save() == data


def test_labels():
    """
    Test the BMG.labels attribute
    """

    # Try loading a BMG containing example labels
    data = (FILES_PATH / 'labels.bmg').read_bytes()
    assert ndspy.bmg.BMG(data).labels == LABELS

    # Make a new BMG with the same labels and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.labels = LABELS
    assert new_bmg.save() == data


def test_messages():
    """
    Test the BMG.messages attribute
    """

    # Uh... test having multiple messages, I guess? All the more
    # interesting things are tested by other functions.

    # Try loading a BMG containing example messages
    data = (FILES_PATH / 'messages.bmg').read_bytes()
    bmg = ndspy.bmg.BMG(data)
    assert [m.stringParts[0] for m in bmg.messages] == STRINGS

    # Make a new BMG with the same messages and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.messages = [ndspy.bmg.Message(b'', s) for s in STRINGS]
    assert new_bmg.save() == data

    # Note: BMGs with null messages are tested by test_Message_isNull()


def test_scripts():
    """
    Test the BMG.scripts attribute
    """

    # Try loading a BMG containing example scripts
    data = (FILES_PATH / 'scripts.bmg').read_bytes()
    assert ndspy.bmg.BMG(data).scripts == SCRIPTS

    # Make a new BMG with the same scripts and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.scripts = SCRIPTS
    assert new_bmg.save() == data


def test_unks():
    """
    Test BMG.unk14, BMG.unk18, and BMG.unk1C
    """

    # Try loading a BMG with some nonzero values for the unks
    data = (FILES_PATH / 'unks.bmg').read_bytes()
    bmg = ndspy.bmg.BMG(data)
    assert bmg.unk14 == 0x01234567
    assert bmg.unk18 == 0x89ABCDEF
    assert bmg.unk1C == 0x02468ACE

    # Make a new BMG with the same unk values and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.unk14 = 0x01234567
    new_bmg.unk18 = 0x89ABCDEF
    new_bmg.unk1C = 0x02468ACE
    assert new_bmg.save() == data


def test_fromMessages():
    """
    Test the BMG.fromMessages() constructor
    """

    # Calling with no arguments should be a TypeError
    with pytest.raises(TypeError):
        ndspy.bmg.BMG.fromMessages()
    # (Including if you give it an ID)
    with pytest.raises(TypeError):
        ndspy.bmg.BMG.fromMessages(id=7)

    # From here on I'll alternate between giving it the id=X
    # keyword-only argument and not.

    # One-argument form
    bmg = ndspy.bmg.BMG.fromMessages(MESSAGES)
    assert bmg.messages is MESSAGES
    assert bmg.instructions == bmg.labels == bmg.scripts == []
    assert bmg.id == 0

    # Two-argument form
    bmg = ndspy.bmg.BMG.fromMessages(MESSAGES, INSTRUCTIONS, id=7)
    assert bmg.messages is MESSAGES
    assert bmg.instructions is INSTRUCTIONS
    assert bmg.labels == bmg.scripts == []
    assert bmg.id == 7

    # Three-argument form
    bmg = ndspy.bmg.BMG.fromMessages(MESSAGES, INSTRUCTIONS, LABELS)
    assert bmg.messages is MESSAGES
    assert bmg.instructions is INSTRUCTIONS
    assert bmg.labels is LABELS
    assert bmg.scripts == []
    assert bmg.id == 0

    # Four-argument form
    bmg = ndspy.bmg.BMG.fromMessages(MESSAGES, INSTRUCTIONS, LABELS, SCRIPTS, id=7)
    assert bmg.messages is MESSAGES
    assert bmg.instructions is INSTRUCTIONS
    assert bmg.labels is LABELS
    assert bmg.scripts == SCRIPTS
    assert bmg.id == 7

    # There's no five-argument form
    with pytest.raises(TypeError):
        ndspy.bmg.BMG.fromMessages(MESSAGES, INSTRUCTIONS, LABELS, SCRIPTS, [])


def test_fromFile():
    """
    Test the BMG.fromFile() constructor
    """
    FP = (FILES_PATH / 'messages.bmg')

    # Load one BMG from a bytes object...
    bmg_A = ndspy.bmg.BMG(FP.read_bytes())

    # Load another with fromFile() using a pathlib.Path...
    assert isinstance(FP, pathlib.Path)
    bmg_B = ndspy.bmg.BMG.fromFile(FP)

    # Load another with fromFile() using a string
    bmg_C = ndspy.bmg.BMG.fromFile(str(FP))

    # Check that they're all equal
    assert bmg_A.messages
    assert (   [m.stringParts[0] for m in bmg_A.messages]
            == [m.stringParts[0] for m in bmg_B.messages]
            == [m.stringParts[0] for m in bmg_C.messages])

    # (The optional "id" parameter is checked by test_id().)


# No need to test save(); we've kind of been using it in almost every
# test function already...


def test_saveToFile(tmp_path):
    """
    Test BMG.saveToFile()
    """
    # Load BMG
    bmg = ndspy.bmg.BMG.fromFile(FILES_PATH / 'messages.bmg')

    fpPath = tmp_path / 'test.bmg'

    # Test with both str's and pathlib.Path's
    for fp in [str(fpPath), fpPath]:

        # Save it there
        bmg.saveToFile(fp)

        # Load it back
        bmg_reloaded = ndspy.bmg.BMG.fromFile(fp)

        # Ensure equality
        assert bmg.messages
        assert (   [m.stringParts[0] for m in bmg.messages]
                == [m.stringParts[0] for m in bmg_reloaded.messages])

        # Clear the file contents so as to not taint the next loop
        # iteration
        fpPath.write_bytes(b'')


def test_Message():
    """
    Test the Message() constructor
    """

    # Zero-argument form
    msg = ndspy.bmg.Message()
    assert msg.info == b''
    assert msg.stringParts == []
    assert msg.isNull == False

    # One-argument form
    msg = ndspy.bmg.Message(b'abc')
    assert msg.info == b'abc'
    assert msg.stringParts == []
    assert msg.isNull == False

    # Two-argument form
    msg = ndspy.bmg.Message(b'abc', STRINGS)
    assert msg.info == b'abc'
    assert msg.stringParts == STRINGS
    assert msg.isNull == False

    # Three-argument form
    # (note: null messages should have empty stringParts)
    msg = ndspy.bmg.Message(b'abc', [], True)
    assert msg.info == b'abc'
    assert msg.stringParts == []
    assert msg.isNull == True

    # No such thing as a four-argument form
    with pytest.raises(TypeError):
        ndspy.bmg.Message(b'abc', [], True, 7)

    # Check that the special-case for wrapping a string in a list works
    # as advertised
    assert ndspy.bmg.Message(7, 'abc').stringParts == ['abc']


def test_Message_info():
    """
    Test the Message.info attribute
    """
    # Try loading a BMG containing messages with example infos
    data = (FILES_PATH / 'message_infos.bmg').read_bytes()
    bmg = ndspy.bmg.BMG(data)
    assert [m.info for m in bmg.messages] == MESSAGE_INFOS

    # Make a new BMG with the same messages/infos and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.messages = [ndspy.bmg.Message(inf, s) for inf, s in zip(MESSAGE_INFOS, STRINGS)]
    assert new_bmg.save() == data

    # Also, ensure that inconsistent Message.info lengths are detected
    bmg = ndspy.bmg.BMG()
    bmg.messages = [ndspy.bmg.Message(b'\1'), ndspy.bmg.Message(b'\1\2')]
    with pytest.raises(ValueError):
        bmg.save()


def test_Message_isNull():
    """
    Test the Message.isNull attribute
    """
    # Try loading a BMG containing messages with a null message
    data = (FILES_PATH / 'message_isnull.bmg').read_bytes()
    bmg = ndspy.bmg.BMG(data)
    assert len(bmg.messages) == len(MESSAGES) == 4
    assert bmg.messages[0].isNull == False
    assert bmg.messages[1].isNull == True
    assert bmg.messages[2].isNull == False
    assert bmg.messages[3].isNull == False

    # Make a new BMG with the same messages and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.messages = [ndspy.bmg.Message(b'', s) for s in STRINGS]
    new_bmg.messages[1].isNull = True
    assert new_bmg.save() == data

    # Also, check that it saves as nothing if it's null
    assert ndspy.bmg.Message(b'', ['aaaa', 'bcde'], True).save('cp1252') == b''


def test_Message_stringParts():
    """
    Test the Message.stringParts attribute
    """

    # Try loading a BMG containing a message with multiple parts
    data = (FILES_PATH / 'message_stringparts.bmg').read_bytes()
    bmg = ndspy.bmg.BMG(data)
    for m1, m2 in zip(bmg.messages[0].stringParts, MESSAGE_PARTS):
        if isinstance(m1, str):
            assert m1 == m2
        else:
            assert m1.type == m2.type
            assert m1.data == m2.data

    # Make a new BMG with the same message and see if it matches
    new_bmg = ndspy.bmg.BMG()
    new_bmg.messages = [ndspy.bmg.Message(b'', MESSAGE_PARTS)]
    assert new_bmg.save() == data


# No need to test Message.save(); we've kind of been using it implicitly
# in lots of test functions already...


def test_Escape_constructor():
    """
    Test the Message.Escape() constructor
    """

    # Zero-argument form
    esc = ndspy.bmg.Message.Escape()
    assert esc.type == 0
    assert esc.data == b''

    # One-argument form
    esc = ndspy.bmg.Message.Escape(7)
    assert esc.type == 7
    assert esc.data == b''

    # Two-argument form
    esc = ndspy.bmg.Message.Escape(7, b'abc')
    assert esc.type == 7
    assert esc.data == b'abc'

    # No such thing as a three-argument form
    with pytest.raises(TypeError):
        ndspy.bmg.Message.Escape(7, b'abc', 8)


def test_Escape_save():
    """
    Test Escape.save()
    """

    # Binary format:
    # - U+001A, in the requested encoding
    # - total length (1 byte)
    # - "type" value (1 byte)
    # - data

    # Empty escape
    esc = ndspy.bmg.Message.Escape(0, b'')
    #                              (U+001A      len   type  data)
    assert esc.save('cp1252')   == (b'\x1A'     b'\3' b'\0' b'')
    assert esc.save('utf-16le') == (b'\x1A\x00' b'\4' b'\0' b'')
    assert esc.save('utf-16be') == (b'\x00\x1A' b'\4' b'\0' b'')

    # An escape with some actual things
    esc = ndspy.bmg.Message.Escape(0xFF, b'abcdefg')
    #                              (U+001A      len     type    data)
    assert esc.save('cp1252')   == (b'\x1A'     b'\x0A' b'\xFF' b'abcdefg')
    assert esc.save('utf-16le') == (b'\x1A\x00' b'\x0B' b'\xFF' b'abcdefg')
    assert esc.save('utf-16be') == (b'\x00\x1A' b'\x0B' b'\xFF' b'abcdefg')
