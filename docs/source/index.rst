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

ndspy
=====

.. image:: https://img.shields.io/discord/534221996230180884.svg?logo=discord&logoColor=white&colorB=7289da
    :alt: Discord
    :target: https://discord.gg/RQhxAxw

.. image:: https://img.shields.io/badge/repo-GitHub-brightgreen.svg?logo=github&logoColor=white
    :alt: GitHub
    :target: https://github.com/RoadrunnerWMC/ndspy

.. image:: https://img.shields.io/pypi/v/ndspy.svg?logo=python&logoColor=white
    :alt: PyPI
    :target: https://pypi.org/project/ndspy/

.. image:: https://img.shields.io/github/license/RoadrunnerWMC/ndspy.svg?logo=gnu&logoColor=white
    :alt: License: GNU GPL 3.0
    :target: https://www.gnu.org/licenses/gpl-3.0

**ndspy** ("en-dee-ESS-pie") is a Python library and suite of command-line
tools that can help you read, modify and create many types of files used in
Nintendo DS games.

ndspy follows a few key design principles:

-   **Accuracy**: ndspy should be able to open and resave any supported file
    with byte-for-byte accuracy if it's in its canonical format
    [#canonical-format]_.
-   **Flexibility**: ndspy should be able to read any valid file in a format it
    supports. In cases where there's a high chance it will be unable to fully
    interpret some especially complex part of a file, it should still be useful
    for editing the other parts.
-   **Semantic**: ndspy's APIs should closely match the semantics of file
    structures while hiding their binary-level details.

ndspy provides both a Python API and a set of simple command-line tools that
make use of it. The command-line tools let you convert files to and from binary
formats without having to write any Python code yourself [#cli-tools]_. The API
is suitable for use in applications written in Python, and in scripts to do
more complex tasks than the command-line tools are capable of.

As ndspy is written in pure Python, it is cross-platform and should run on all
platforms Python supports. Note that Python doesn't support the Nintendo DS
itself; ndspy is intended to be used on your PC.

Interested? Read on to see some examples, or check the :doc:`api/index` to see
the documentation for a specific module. When you're ready to install, head
over to the :ref:`installation` section!

.. note::
    If you plan to use ndspy to work with sound data and you aren't yet
    familiar with *SDAT* files, consider reading :doc:`the appendix explaining
    how they're structured <appendices/sdat-structure>` first.

.. [#canonical-format]
    That is, if it's arranged in the way that files in that format usually are.
    Although it's often possible to arrange a file in many different ways and
    still have it be valid, ndspy only aims for byte-for-byte output accuracy
    with files that are arranged in the most common way.

.. [#cli-tools]
    Unfortunately, the command-line tools are sorely lacking in both substance
    and documentation at the moment. I hope to improve these in the
    not-too-distant future!


A few examples of ndspy in action
---------------------------------

.. testsetup:: *

    import os, os.path
    import shutil
    import tempfile

    origCwd = os.getcwd()
    dir = tempfile.TemporaryDirectory()
    os.chdir(dir.name)

    if haveNSMB:
        shutil.copyfile(nsmbRomPath, 'nsmb.nds')

    shutil.copyfile(testFilesPath / 'never-gonna-give-you-up.sseq',
                    'never-gonna-give-you-up.sseq')

.. testcleanup:: *

    os.chdir(origCwd)
    dir.cleanup()

Create a *BMG* file containing message strings:

.. doctest::

    >>> import ndspy.bmg
    >>> message1 = ndspy.bmg.Message(b'', ['Open your eyes...'])
    >>> message2 = ndspy.bmg.Message(b'', ['Wake up, Link...'])
    >>> bmg = ndspy.bmg.BMG.fromMessages([message1, message2])
    >>> bmg.save()
    b'MESGbmg1\xa0\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00INF1 \x00\x00\x00\x02\x00\x04\x00\x00\x00\x00\x00\x02\x00\x00\x00&\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00DAT1`\x00\x00\x00\x00\x00O\x00p\x00e\x00n\x00 \x00y\x00o\x00u\x00r\x00 \x00e\x00y\x00e\x00s\x00.\x00.\x00.\x00\x00\x00W\x00a\x00k\x00e\x00 \x00u\x00p\x00,\x00 \x00L\x00i\x00n\x00k\x00.\x00.\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    >>>

Change all notes in a *SSEQ* sequenced music file to middle C, similar to `this
song <https://youtu.be/cSAp9sBzPbc>`_:

.. doctest::

    >>> import ndspy.soundSequence
    >>> song = ndspy.soundSequence.SSEQ.fromFile('never-gonna-give-you-up.sseq')
    >>> song.parse()
    >>> for event in song.events:
    ...     if isinstance(event, ndspy.soundSequence.NoteSequenceEvent):
    ...         event.pitch = 60
    ...
    >>> song.saveToFile('never-gonna-give-you-up-but-all-the-notes-are-c.sseq')
    >>>

Compress and decompress data using the *LZ10* compression format:

.. doctest::

    >>> import ndspy.lz10
    >>> compressed = ndspy.lz10.compress(b'This is some data to compress')
    >>> compressed
    b'\x10\x1d\x00\x00\x04This \x00\x02so\x00me data \x00to compr\x00ess\x00\x00\x00\x00\x00'
    >>> ndspy.lz10.decompress(compressed)
    b'This is some data to compress'
    >>>

Search for all files starting with a particular byte sequence in a ROM:

.. doctest::
    :skipif: not haveNSMB

    >>> import ndspy.rom
    >>> rom = ndspy.rom.NintendoDSRom.fromFile('nsmb.nds')
    >>> for i, file in enumerate(rom.files):
    ...     if file.startswith(b'BMD0'):
    ...         print(rom.filenames[i] + ' is a NSBMD model')
    ...
    demo/end_kp.nsbmd is a NSBMD model
    demo/staffroll.nsbmd is a NSBMD model
    demo/staffroll_back.nsbmd is a NSBMD model
    enemy/A_jiku.nsbmd is a NSBMD model
    enemy/all_goal_flag.nsbmd is a NSBMD model
    ...
    map/world7.nsbmd is a NSBMD model
    map/world8.nsbmd is a NSBMD model
    >>>


Misconceptions
--------------

Still a little confused about what exactly ndspy is or what it's capable of?
This section will try to answer some questions you may have.

*   ndspy is a *library*, not a *program.* To use ndspy, you have to write your
    own Python code; ndspy is essentially a tool your code can use. This may
    sound daunting -- especially if you're not very familiar with Python -- but
    the :doc:`tutorials/index` walk you through this process step-by-step for
    some common tasks. In the future, I plan to add some command-line and
    maybe even GUI tools powered by ndspy, but until then, this is how you use
    it.
*   ndspy runs on your PC, not on the Nintendo DS itself. You use it to create
    and modify game files, which can then be run on the console. DS games have
    to be written in a compiled language such as C or C++ to have any hope of
    being efficient; Python will never be a serious option there,
    unfortunately.


.. _installation:

Installation
------------

ndspy requires Python 3.6 or newer to run [#pypy-3.5]_. Python 2 is not
supported at all.

The easiest way to get the latest stable release of ndspy is through PyPI using
pip.

pip is a command-line application, so you'll need to use the Windows command
prompt or bash to do this. The exact command you need to enter depends on your
operating system and the settings you chose when you installed Python. One of
the following possibilities will probably work for you, though:

.. code-block:: text

    pip install ndspy

    python3 -m pip install ndspy

    py -3 -m pip install ndspy

If you want the very latest version of ndspy including features and bugfixes
not yet in any official release, you can also download the code from the
`GitHub repository <https://github.com/RoadrunnerWMC/ndspy>`_ and install it
manually. Note that `crcmod <https://pypi.org/project/crcmod/>`_ is a required
dependency.

.. [#pypy-3.5]
    PyPy3.5 v6.0 or newer should also work, due to its
    anachronistic-yet-appreciated support for f-strings (introduced in Python
    3.6). However, setuptools (pip) will refuse to install ndspy in PyPy3.5
    because it doesn't know that f-strings is the only feature ndspy needs from
    3.6. As a workaround, you can download the ndspy source code folder and put
    it in your PyPy's site-packages folder manually.

Support
-------

I spent a long time writing the documentation for ndspy, so first please
double-check that your question isn't already answered in the :doc:`api/index`
or :doc:`tutorials/index`.

If that doesn't help, you can ask me (RoadrunnerWMC) your questions via `the
ndspy Discord server <https://discord.gg/RQhxAxw>`_. I'll try to get back to
you as quickly as I can!

If you think you've found a bug in ndspy, please `file an issue on GitHub
<https://github.com/RoadrunnerWMC/ndspy/issues/new>`_. Thanks!


Versioning
----------

ndspy follows `semantic versioning <https://semver.org/>`_ to the best of my
ability. If a tool claims to work with ndspy 1.0.2, it should also work with
ndspy 1.2.0, but not necessarily 2.0.0. (Please note that not all of those
version numbers actually exist!)

Undocumented modules are considered exempt from semantic versioning, and are
subject to drastic changes at any time. This is also mentioned in the
:ref:`undocumented-apis` section.


.. https://stackoverflow.com/a/16302843

.. toctree::
    :maxdepth: 2
    :caption: Contents

    Home <self>
    tutorials/index
    api/index
    tools/index
    changelog
    appendices/sdat-structure


Credits
-------

**ndspy** was written by `RoadrunnerWMC <https://github.com/RoadrunnerWMC/>`_,
using information from many, many sources. In alphabetical order:

*   `Source code for apicula <https://github.com/scurest/apicula>`_ -- a very
    nice reference for information about *NSBMD*
*   `Custom Mario Kart Wiiki <http://wiki.tockdom.com/>`_ -- for information on
    the version of *BMG* files used in Wii games (which isn't the same as the
    version of *BMG* used in DS games, but is similar)
*   `DS Sound Studio <http://archive.dshack.org/thread.php?tid=2590>`_ -- for
    the meaning of sequence players and stream players
*   `Source code for DSDecmp <https://github.com/Barubary/dsdecmp>`_ (`homepage
    <http://www.romhacking.net/utilities/789/>`_) -- for code for several
    compression formats
*   `DSiBrew <http://www.dsibrew.org/>`_ -- for some more information about the
    ROM file format
*   Personal correspondence with Eugene#6990 on Discord -- for information
    about PSG instruments in *SBNK* files
*   `GBATEK <http://problemkaputt.de/gbatek.htm>`_ -- for various miscellaneous
    things
*   Personal correspondence with Gota7#9350 on Discord -- for information about
    note definition type values in *SBNK* files
*   `Imran Nazar: The Smallest NDS File
    <http://imrannazar.com/The-Smallest-NDS-File>`_ -- convenient quick
    reference for the ROM header format; also provides a nice test case for the
    ROM library code
*   `kiwi.ds Nitro Composer File (*.sdat) Specification
    <https://sites.google.com/site/kiwids/sdat.html>`_ -- probably the best
    overall reference for *SDAT*
*   `NDSTech Wiki (archived)
    <https://web.archive.org/web/20110106014930/http://www.bottledlight.com/ds/index.php/FileFormats/NDSFormat>`_
    -- for some more information about the ROM file format
*   `Nintendo DS File Formats
    <http://www.romhacking.net/documents/[469]nds_formats.htm>`_ -- a terrific
    reference for a wide variety of format specifications
*   `Source code for Nintendo DS/GBA Compressors by CUE
    <http://www.romhacking.net/utilities/826/>`_ (`thread
    <https://gbatemp.net/threads/nintendo-ds-gba-compressors.313278/>`_) -- for
    code for reversed LZ compression (code compression)
*   `Source code for NSMB Editor (NSMBe)
    <https://github.com/Dirbaio/NSMB-Editor>`_ -- for information and code for
    many formats
*   `Source code for sseq2mid
    <https://github.com/loveemu/loveemu-lab/tree/master/sseq2mid/src2>`_ --
    supports more types of sequence events than are documented in other
    references
*   `Source code for Tinke <https://github.com/pleonex/tinke>`_ -- fills in the
    gaps in *SDAT* where the other references are ambiguous
*   Some original research by me and `Skawo
    <https://www.youtube.com/user/skawo90>`_.

Thank you to everyone who wrote these sources!


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. todo::

    It'd be great to add an example or two to the top of every module.

    Functions for loading/saving BMG to/from `wbmgt format
    <https://szs.wiimm.de/info/bmg-text.html>`_?

    The tools need a lot of work, and documentation.

    Automated testing.

    Write tutorials.

    Try running the SSEQ/SSAR parser on all ROMs to identify issues.

    ROM secure area en/decryption, ported from ndstool
