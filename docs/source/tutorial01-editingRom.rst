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

Tutorial 1: Editing a File in a ROM
===================================

.. py:currentmodule:: ndspy.rom

This tutorial will explain the process of opening a ROM file, extracting a file
from it, putting a modified version of the file back into the ROM, and saving
the modified ROM.

.. note::

    We're going to do this the way I would personally do it -- by making small
    temporary scripts that accomplish whatever we need. To make it easier to
    follow, I'll post the entire script file every time it changes, instead of
    just the edited parts. (The modified lines will be highlighted, though.)


Opening the ROM
---------------

The first step will be to import the ndspy module dedicated to ROM files,
:py:mod:`ndspy.rom`. Make a new, empty Python file (say,
``rom_files_tutorial.py``), open it, and write the following:

.. code-block:: python
    :linenos:

    import ndspy.rom

Try running it at this point. If it finishes without any errors, everything's
good so far.

Of course, we need to have a ROM to use. For ease of access, it's a good idea
to put it in the same folder as your Python script. I'll be using *New Super
Mario Bros.* (``nsmb.nds``), but the same technique will work on just about any
ROM.

:py:mod:`ndspy.rom` provides a class that we can use to work with ROM files:
:py:class:`NintendoDSRom`. Its constructor takes a :py:class:`bytes` object
containing the ROM file data, so we'll need to get one of those. This step
doesn't really involve ndspy per se:

.. code-block:: python
    :emphasize-lines: 3-4
    :linenos:

    import ndspy.rom

    with open('nsmb.nds', 'rb') as f:
        data = f.read()

``'rb'`` there tells ``open()`` to open the file for ``r``\ eading in
``b``\ inary mode. We can print the beginning of the data to see what it looks
like:

.. code-block:: python
    :emphasize-lines: 6
    :linenos:

    import ndspy.rom

    with open('nsmb.nds', 'rb') as f:
        data = f.read()

    print(data[:50])

.. code-block:: text

    b'NEW MARIO\x00\x00\x00A2DE01\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x08\x00\x02\x00\x00\x00\x02\xa4\xef\x05\x00\x00\xe8'

Now we can hand it off to ndspy to get a :py:class:`NintendoDSRom` object we
can do interesting things with:

.. code-block:: python
    :emphasize-lines: 6-8
    :linenos:

    import ndspy.rom

    with open('nsmb.nds', 'rb') as f:
        data = f.read()

    rom = ndspy.rom.NintendoDSRom(data)

    print(rom)

.. code-block:: text

    <rom "NEW MARIO" (A2DE)>

Cool, we now have a :py:class:`NintendoDSRom` for NSMB. (``NEW MARIO`` is the
game's internal name. Internal names can be helpful, but they don't always
necessarily match up with a game's actual name.)

Since opening a file, reading its contents as a :py:class:`bytes` object, and
making a :py:class:`NintendoDSRom` from it is a very common thing to do, ndspy
provides a shortcut for this:

.. code-block:: python
    :emphasize-lines: 3
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    print(rom)

.. code-block:: text

    <rom "NEW MARIO" (A2DE)>

As you can see, that does the same thing as what we did on our own. Many ndspy
classes have ``.fromFile(filename)`` functions like this!

Now that we have a ROM object, what can we do with it? Lots of things! For
example, we can see how many files it contains:

.. code-block:: python
    :emphasize-lines: 5
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    print(len(rom.files))

.. code-block:: text

    2088

Or we can check what memory address the main ARM9 code file will be loaded to:

.. code-block:: python
    :emphasize-lines: 5
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    print(hex(rom.arm9RamAddress))

.. code-block:: text

    0x2000000

But of course, what we really want to do is extract a file.


Extracting a file
-----------------

I'm going to extract ``polygon_unit/evf_cloud1.nsbtx``, which is the texture
for the foreground clouds in World 7-1.

.. figure:: images/tutorial-rom-before.png
    :scale: 30%
    :align: center

    What World 7-1 looks like in regular *New Super Mario Bros.* You can see
    one-and-a-half foreground clouds in this screenshot.

Before continuing, you need to understand the relationship between files,
filenames, and file IDs in ROMs. There's an explanation in the introductory
material for the :py:mod:`ndspy.fnt` module (which is used internally by
:py:mod:`ndspy.rom`) which I recommend you read:
:ref:`file-names-and-file-ids`. What you really need to know, though, is that
files are fundamentally accessed by ID, and IDs are indices into a list of all
files in the ROM. Filename tables are separate, exist only for convenience, and
simply map file (and folder) names to file IDs.

So we need to get the file ID for ``polygon_unit/evf_cloud1.nsbtx``. A
:py:class:`NintendoDSRom`'s filenames table is provided as a
:py:class:`ndspy.fnt.Folder`, in a ``.filenames`` attribute. We can print that
out to show all of the filenames and their corresponding file IDs (warning:
this is a pretty long printout):

.. code-block:: python
    :emphasize-lines: 5
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    print(rom.filenames)

.. code-block:: text

    0131 00DUMMY
    0132 BUILDTIME
    0133 mgvs_sound_data.sdat
    0134 sound_data.sdat
    0135 ARCHIVE/
    0135     ARC0.narc
    0136     bomthrow.narc
    0137     card.narc
      [snip]
    1896     pl_ttl_LZ.bin
    1897     plnovs_LZ.bin
    1898 polygon_unit/
    1898     evf_cloud1.nsbtx
    1899     evf_haze1.nsbtx
    1900     evf_sea1_a.nsbtx
      [snip]
    2085     UI_O_menu_title_logo_o_u_ncg.bin
    2086     UI_O_menu_title_logo_u.bncl
    2087     UI_O_menu_title_o_d_ncg.bin

From this, we can see that the file ID for ``polygon_unit/evf_cloud1.nsbtx`` is
1898. How would we get that programmatically, though? Pretty easily, actually:

.. code-block:: python
    :emphasize-lines: 5
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    print(rom.filenames.idOf('polygon_unit/evf_cloud1.nsbtx'))

.. code-block:: text

    1898

ndspy again provides a shortcut for this: :py:class:`ndspy.fnt.Folder`\s
support indexing syntax for converting between filenames and file IDs. We can
use that here to make the code a bit shorter:

.. code-block:: python
    :emphasize-lines: 5
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    print(rom.filenames['polygon_unit/evf_cloud1.nsbtx'])

.. code-block:: text

    1898

Now we can simply get the data for that file by using that file ID as an index
into the ROM's ``.files`` attribute:

.. code-block:: python
    :emphasize-lines: 5-8
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    cloudNSBTXFileID = rom.filenames['polygon_unit/evf_cloud1.nsbtx']
    cloudNSBTX = rom.files[cloudNSBTXFileID]

    print(cloudNSBTX[:50])

.. code-block:: text

    bytearray(b'BTX0\xff\xfe\x01\x00\x84a\x00\x00\x10\x00\x01\x00\x14\x00\x00\x00TEX0pa\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x00\x00\x00\x00\x90\x00\x00\x00\x00\x00\x00\x00\x00\x08')

Cool.

.. note::

    You might be wondering what this "``bytearray``" is, and why we didn't get
    a :py:class:`bytes` object. A :py:class:`bytearray` is essentially a
    mutable version of :py:class:`bytes`, meaning it can be modified. ndspy
    provides the data for files within the ROM as :py:class:`bytearray`\s to
    make it a bit more convenient to edit them.

Since it's pretty common to want to get the data for the file with some
filename, ndspy yet again has a shortcut for it:

.. code-block:: python
    :emphasize-lines: 5
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    cloudNSBTX = rom.getFileByName('polygon_unit/evf_cloud1.nsbtx')

    print(cloudNSBTX[:50])

.. code-block:: text

    bytearray(b'BTX0\xff\xfe\x01\x00\x84a\x00\x00\x10\x00\x01\x00\x14\x00\x00\x00TEX0pa\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x00\x00\x00\x00\x90\x00\x00\x00\x00\x00\x00\x00\x00\x08')

.. note::

    At this point, you're probably wishing I would just jump straight to the
    shortcut syntax in the first place. Well, I think it's important to have
    some idea of what the shortcuts are shortcuts *for*, especially since you
    won't always be able to use them in every situation. For example, the
    ``.fromFile(filename)`` functions aren't very useful if you want to load a
    file that you got from a ROM. ROM files are provided as :py:class:`bytes`
    objects, so you're better off using class constructors that take those
    instead.

Anyway, now we can go ahead and save ``evf_cloud1.nsbtx`` to an actual file
outside of the ROM:

.. code-block:: python
    :emphasize-lines: 7-8
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    cloudNSBTX = rom.getFileByName('polygon_unit/evf_cloud1.nsbtx')

    with open('evf_cloud1.nsbtx', 'wb') as f:
        f.write(cloudNSBTX)

Now you can open that file with some other tool (such as `MKDS Course Modifier
<https://www.romhacking.net/utilities/1285/>`_) and make changes as you see
fit.

Go ahead and do that now. I'll wait.


Replacing a file
----------------

Done? Time to replace the file in the ROM with our new copy, then!

Let's suppose you saved the modified NSBTX file to ``evf_cloud1_edited.nsbtx``.
Our goal is to get that as a :py:class:`bytes` object and put it into
``rom.files``. One step at a time, though -- let's start by getting the new
file data:

.. code-block:: python
    :emphasize-lines: 5-6
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    with open('evf_cloud1_edited.nsbtx', 'rb') as f:
        cloudNSBTXEdited = f.read()

This gets us the NSBTX data and puts it in ``cloudNSBTXEdited``. We can put
said data into the ``files`` list using the file ID:

.. code-block:: python
    :emphasize-lines: 8
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    with open('evf_cloud1_edited.nsbtx', 'rb') as f:
        cloudNSBTXEdited = f.read()

    rom.files[rom.filenames['polygon_unit/evf_cloud1.nsbtx']] = cloudNSBTXEdited

Or with ndspy's shortcut function for accomplishing the same thing:

.. code-block:: python
    :emphasize-lines: 8
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    with open('evf_cloud1_edited.nsbtx', 'rb') as f:
        cloudNSBTXEdited = f.read()

    rom.setFileByName('polygon_unit/evf_cloud1.nsbtx', cloudNSBTXEdited)

Done. All that's left now is to save the modified ROM so we can try it out!


Saving the ROM
--------------

:py:class:`NintendoDSRom` provides a ``.save()`` function that returns a
:py:class:`bytes` object, which we can use to save the ROM:

.. code-block:: python
    :emphasize-lines: 10-11
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    with open('evf_cloud1_edited.nsbtx', 'rb') as f:
        cloudNSBTXEdited = f.read()

    rom.setFileByName('polygon_unit/evf_cloud1.nsbtx', cloudNSBTXEdited)

    with open('nsmb_edited.nds', 'wb') as f:
        f.write(rom.save())

Naturally, though, there's a shortcut for that:

.. code-block:: python
    :emphasize-lines: 10
    :linenos:

    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')

    with open('evf_cloud1_edited.nsbtx', 'rb') as f:
        cloudNSBTXEdited = f.read()

    rom.setFileByName('polygon_unit/evf_cloud1.nsbtx', cloudNSBTXEdited)

    rom.saveToFile('nsmb_edited.nds')

And that's all there is to it! Go try your ROM out and enjoy whatever change
you made.

.. figure:: images/tutorial-rom-after.png
    :scale: 30%
    :align: center

    Perfect.
