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

Tutorial 2: Editing a File in a NARC Archive
============================================

.. py:currentmodule:: ndspy.narc

This tutorial will explain the process of opening a *NARC* archive file,
extracting a file from it, putting a modified version of the file back into the
*NARC* archive, and saving the modified ROM.

If you've completed the first tutorial (:doc:`rom-editing`), this will feel
extremely familiar. *NARC*\s are more-or-less like miniature ROMs that only
have files and filenames, so the ndspy APIs for ROMs and *NARC*\s are very
similar.

.. seealso::

    If you haven't tried the first two tutorials yet, I recommend you do so:

    *   :doc:`getting-started`: This tutorial helps you check that you have
        ndspy installed and set up correctly.
    *   :doc:`rom-editing`: This one is written at a slower pace than the other
        tutorials, and serves as a gentle introduction to help you get a feel
        for how to use ndspy in general.


Opening the NARC
----------------

We'll begin by importing :py:mod:`ndspy.narc`, the ndspy module for *NARC*
archives. Make a new, empty Python file (say,
``narc_files_tutorial.py``), and put the following in it:

.. code-block:: python
    :linenos:

    import ndspy.narc

You can test it at this point if you want to check that it runs correctly, but
it won't do a whole lot!

Next, we need to open a *NARC* using the :py:class:`NARC` class. If your *NARC*
is within a ROM file, you can use :py:mod:`ndspy.rom` to get the *NARC* data
and pass it to :py:class:`NARC`\'s default constructor, like so:

.. code-block:: python
    :emphasize-lines: 2, 4-6
    :linenos:

    import ndspy.narc
    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom('nsmb.nds')
    narcData = rom.files[169]
    narc = ndspy.narc.NARC(narcData)

However, for brevity, I'll be assuming from here on that your *NARC* is a
standalone file, so that I can use the :py:func:`fromFile` class method to load
it in a single line instead:

.. code-block:: python
    :emphasize-lines: 3
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

You can substitute the ROM-loading code if you prefer, though, of course.

Either way, now we have a :py:class:`NARC` object. We can print it out to see
all of its file IDs, folders and filenames, and the first few bytes of each
file:

.. code-block:: python
    :emphasize-lines: 4
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')
    print(narc)

.. code-block:: text

    <narc endiannessOfBeginning='>'
        0000 vs_escape/
        0000     d_2d_mgvs_bg_escape_down_ncg.bin    b'\x10\0\x80\0?\0\0\xf0\1\xf0\x13\xf0%\xf07\xf0'...
        0001     d_2d_mgvs_bg_escape_down_ncl.bin    b'\x1f\03\tU\t:\1\x97\tz\5\x9b\5\xb9\r'...
        0002     d_2d_mgvs_bg_escape_down_nsc.bin    b'\x10\0\x08\0\0\x90\x82\x91\xe2\x92\x82\x93\x82\0\x94\xe2'...
        0003     d_2d_mgvs_bg_escape_up1_nsc.bin     b'\x10\0\x08\0\0\xc7\xa1\xc8\xa1\xc9\xb1\xca\x91\0\xcb\x81'...
        0004     d_2d_mgvs_bg_escape_up2_nsc.bin     b'\x10\0\x08\0 \x7f3\xf0\1\xfb5\xfa5\xf9\05'...
        0005     d_2d_mgvs_bg_escape_up3_nsc.bin     b'\x10\0\x08\00\x7f3\xf0\1p\1\x96\xd5\x96\xd1\xe0'...
        0006     d_2d_mgvs_bg_escape_up_ncg.bin      b'\x10\0\x80\0?\0\0\xf0\1\xf0\x13\xf0%\xf07\xf0'...
        0007     d_2d_mgvs_bg_escape_up_ncl.bin      b'\x94z\0\0\0\0\0\0\0\0\0\0\0\0\0\0'...
        0008     d_2d_mgvs_escape_ncg.bin            b'\x10\0@\06\0\0\xf0\1\x80\x130\xf0\x1fp1'...
        0009     d_2d_mgvs_escape_ncl.bin            b'\xa7}\0\0\xff\x7f\x18c\x10B\x08!\xff\3\xbc\2'...
    >

.. note::
    Don't worry about the ``endiannessOfBeginning`` part too much; it just
    means that ndspy noticed that the *NARC* file data had a slightly
    nonstandard header, which it will match when we resave the file.

    If, however, you're planning on making a new :py:class:`NARC` from scratch
    for a game that uses *NARC*\s with these nonstandard headers, you'll have
    to remember to set :py:attr:`NARC.endiannessOfBeginning` to ``'>'``
    yourself!


Extracting a file
-----------------

I'm going to extract ``d_2d_mgvs_escape_ncg.bin`` and
``d_2d_mgvs_escape_ncl.bin``, which are the sprite graphics and palette for
*New Super Mario Bros.'s* "Danger, Bob-omb! Danger!" minigame.

.. figure:: images/narc-before.png
    :scale: 30%
    :align: center

    What the minigame looks like in regular *New Super Mario Bros.* You use the
    touch screen to drag the Bob-Omb around, and dodge the fire columns and
    fireballs. I wonder if there's a way all of this excess heat could be put
    to good use...

.. note::

    If you're not yet familiar with the relationship between files,
    filenames, and file IDs in *NARC*\s, I recommend you read the documentation
    on this topic in the introductory material for the :py:mod:`ndspy.fnt`
    module (which is used internally by :py:mod:`ndspy.narc`):
    :ref:`file-names-and-file-ids`.

    What you really need to know, though, is that files are fundamentally
    accessed by ID, and IDs are indices into a list of all files in the *NARC*.
    Filename tables are separate, exist only for convenience, and simply map
    file (and folder) names to file IDs.

    It's also worth mentioning that, while *NARC* file IDs work the same way as
    ROM file IDs, they're completely separate from the file IDs of the
    enclosing ROM, if there is one.

We can see from the *NARC* printout we made earlier that these two files have
file IDs 8 and 9 respectively; thus, we can access their data directly using
those indices:

.. code-block:: python
    :emphasize-lines: 5-6
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    ncgData = narc.files[8]
    nclData = narc.files[9]

Or we could use the :py:class:`NARC` class's helper function that looks up a
filename in the filenames table to get a file ID, and retrieves the
corresponding file data directly:

.. code-block:: python
    :emphasize-lines: 5-6
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    ncgData = narc.getFileByName('vs_escape/d_2d_mgvs_escape_ncg.bin')
    nclData = narc.getFileByName('vs_escape/d_2d_mgvs_escape_ncl.bin')

Either way, we've now got :py:class:`bytes` objects containing the data for the
files we're interested in.

Now it's time to edit the files. If ndspy supports editing the file formats in
question, you can just import the appropriate modules and edit the files that
way. (In this particular example case, the *NCL* and *NCG* files can be edited
using the :py:mod:`ndspy.lz10` and :py:mod:`ndspy.graphics2D` modules, which is
what I did at this point.) If you instead want to save the files externally to
edit using some other tool, you can of course do that as well:

.. code-block:: python
    :emphasize-lines: 8-11
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    ncgData = narc.getFileByName('vs_escape/d_2d_mgvs_escape_ncg.bin')
    nclData = narc.getFileByName('vs_escape/d_2d_mgvs_escape_ncl.bin')

    with open('d_2d_mgvs_escape_ncg.bin', 'wb') as f:
        f.write(ncgData)
    with open('d_2d_mgvs_escape_ncl.bin', 'wb') as f:
        f.write(nclData)


Replacing a file
----------------

Once you're done editing your file, we can go ahead and put it back in the
*NARC*.

If (like me) you modified the :py:class:`bytes` objects from the *NARC* using
other ndspy modules, you'll already have the modified file data as
:py:class:`bytes` objects. But if you instead saved your file externally to
edit with something else, you'll need to load its data back in:

.. code-block:: python
    :emphasize-lines: 5-8
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    with open('d_2d_mgvs_escape_ncg_edited.bin', 'rb') as f:
        ncgData = f.read()
    with open('d_2d_mgvs_escape_ncl_edited.bin', 'rb') as f:
        nclData = f.read()

Now we can put the data back into the *NARC*, either by file ID:

.. code-block:: python
    :emphasize-lines: 10-11
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    with open('d_2d_mgvs_escape_ncg_edited.bin', 'rb') as f:
        ncgData = f.read()
    with open('d_2d_mgvs_escape_ncl_edited.bin', 'rb') as f:
        nclData = f.read()

    narc.files[8] = ncgData
    narc.files[9] = nclData

Or by filename:

.. code-block:: python
    :emphasize-lines: 10-11
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    with open('d_2d_mgvs_escape_ncg_edited.bin', 'rb') as f:
        ncgData = f.read()
    with open('d_2d_mgvs_escape_ncl_edited.bin', 'rb') as f:
        nclData = f.read()

    narc.setFileByName('vs_escape/d_2d_mgvs_escape_ncg.bin', ncgData)
    narc.setFileByName('vs_escape/d_2d_mgvs_escape_ncl.bin', nclData)


Saving the NARC
---------------

All that's left now is to resave the *NARC*. If you want to put it into a ROM,
you should use the *NARC*'s ``.save()`` function to get a :py:class:`bytes`,
suitable for the ROM's ``.files`` list:

.. code-block:: python
    :emphasize-lines: 2, 4, 16
    :linenos:

    import ndspy.narc
    import ndspy.rom

    rom = ndspy.rom.NintendoDSRom('nsmb.nds')

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    with open('d_2d_mgvs_escape_ncg_edited.bin', 'rb') as f:
        ncgData = f.read()
    with open('d_2d_mgvs_escape_ncl_edited.bin', 'rb') as f:
        nclData = f.read()

    narc.setFileByName('vs_escape/d_2d_mgvs_escape_ncg.bin', ncgData)
    narc.setFileByName('vs_escape/d_2d_mgvs_escape_ncl.bin', nclData)

    rom.files[169] = narc.save()

(Don't forget to save the ROM itself when you're done with it, too!)

Or if you just want to save it as its own file, that can be done using the
``.saveToFile()`` function:

.. code-block:: python
    :emphasize-lines: 13
    :linenos:

    import ndspy.narc

    narc = ndspy.narc.NARC.fromFile('vs_escape.narc')

    with open('d_2d_mgvs_escape_ncg_edited.bin', 'rb') as f:
        ncgData = f.read()
    with open('d_2d_mgvs_escape_ncl_edited.bin', 'rb') as f:
        nclData = f.read()

    narc.setFileByName('vs_escape/d_2d_mgvs_escape_ncg.bin', ncgData)
    narc.setFileByName('vs_escape/d_2d_mgvs_escape_ncl.bin', nclData)

    narc.saveToFile('vs_escape_edited.narc')

And, well, that's it! Have fun with your newly modified *NARC* file.

.. figure:: images/narc-after.png
    :scale: 30%
    :align: center

    It's supposed to be a pizza, but I'm no good at drawing. At least I tried!
