ndspy
=====

[![Discord](https://img.shields.io/discord/534221996230180884.svg?logo=discord&logoColor=white&colorB=7289da)](https://discord.gg/RQhxAxw)
[![Documentation](https://img.shields.io/badge/documentation-Read%20the%20Docs-brightgreen.svg?logo=read%20the%20docs&logoColor=white)](http://ndspy.readthedocs.io/)
[![PyPI](https://img.shields.io/pypi/v/ndspy.svg?logo=python&logoColor=white)](https://pypi.org/project/ndspy/)
[![License: GNU GPL 3.0](https://img.shields.io/github/license/RoadrunnerWMC/ndspy.svg?logo=gnu&logoColor=white)](https://www.gnu.org/licenses/gpl-3.0)

**ndspy** ("en-dee-ESS-pie") is a Python library and suite of command-line
tools that can help you read, modify and create many types of files used in
Nintendo DS games.

ndspy follows a few key design principles:

-   **Accuracy**: ndspy should be able to open and resave any supported file
    with byte-for-byte accuracy if it's in its canonical format.
-   **Flexibility**: ndspy should be able to read any valid file in a format it
    supports. In cases where there's a high chance it will be unable to fully
    interpret some especially complex part of a file, it should still be useful
    for editing the other parts.
-   **Semantic**: ndspy's APIs should closely match the semantics of file
    structures while hiding their binary-level details.

ndspy provides both a Python API and a set of simple command-line tools that
make use of it. The command-line tools let you convert files to and from binary
formats without having to write any Python code yourself. The API is suitable
for use in applications written in Python, and in scripts to do more complex
tasks than the command-line tools are capable of.

As ndspy is written in pure Python, it is cross-platform and should run on all
platforms Python supports. Note that Python doesn't support the Nintendo DS
itself; ndspy is intended to be used on your PC.

Interested? Read on to see some examples, or check the [API
Reference](https://ndspy.readthedocs.io/en/latest/api/index.html) to see the
documentation for a specific module. When you're ready to install, head over to
the [Installation](#installation) section!



A few examples of ndspy in action
---------------------------------

Create a *BMG* file containing message strings:

```python
>>> import ndspy.bmg
>>> message1 = ndspy.bmg.Message(b'', ['Open your eyes...'])
>>> message2 = ndspy.bmg.Message(b'', ['Wake up, Link...'])
>>> bmg = ndspy.bmg.BMG.fromMessages([message1, message2])
>>> bmg.save()
b'MESGbmg1\xa0\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00INF1 \x00\x00\x00\x02\x00\x04\x00\x00\x00\x00\x00\x02\x00\x00\x00&\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00DAT1`\x00\x00\x00\x00\x00O\x00p\x00e\x00n\x00 \x00y\x00o\x00u\x00r\x00 \x00e\x00y\x00e\x00s\x00.\x00.\x00.\x00\x00\x00W\x00a\x00k\x00e\x00 \x00u\x00p\x00,\x00 \x00L\x00i\x00n\x00k\x00.\x00.\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>>
```

Change all notes in a *SSEQ* sequenced music file to middle C, similar to [this
song](https://youtu.be/cSAp9sBzPbc):

```python
>>> import ndspy.soundSequence
>>> song = ndspy.soundSequence.SSEQ.fromFile('never-gonna-give-you-up.sseq')
>>> song.parse()
>>> for event in song.events:
...     if isinstance(event, ndspy.soundSequence.NoteSequenceEvent):
...         event.pitch = 60
...
>>> song.saveToFile('never-gonna-give-you-up-but-all-the-notes-are-c.sseq')
>>>
```

Compress and decompress data using the *LZ10* compression format:

```python
>>> import ndspy.lz10
>>> compressed = ndspy.lz10.compress(b'This is some data to compress')
>>> compressed
b'\x10\x1d\x00\x00\x04This \x00\x02so\x00me data \x00to compr\x00ess\x00\x00\x00\x00\x00'
>>> ndspy.lz10.decompress(compressed)
b'This is some data to compress'
>>>
```

Search for all files starting with a particular byte sequence in a ROM:

```python
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
```


Misconceptions
--------------

Still a little confused about what exactly ndspy is or what it's capable of?
This section will try to answer some questions you may have.

-   ndspy is a *library*, not a *program.* To use ndspy, you have to write your
    own Python code; ndspy is essentially a tool your code can use. This may
    sound daunting -- especially if you're not very familiar with Python -- but
    the
    [tutorials](https://ndspy.readthedocs.io/en/latest/tutorials/index.html)
    walk you through this process step-by-step for some common tasks. In the
    future, I plan to add some command-line and maybe even GUI tools powered by
    ndspy, but until then, this is how you use it.
-   ndspy runs on your PC, not on the Nintendo DS itself. You use it to create
    and modify game files, which can then be run on the console. DS games have
    to be written in a compiled language such as C or C++ to have any hope of
    being efficient; Python will never be a serious option there,
    unfortunately.
-   ndspy doesn't support every type of file used in every DS game. In fact,
    for any given game, it's likely that the majority of the game's files
    *won't* be supported by ndspy. There's a huge amount of variety in video
    game file formats, and it would be impossible to support them all. ndspy
    focuses on file formats used in many games, especially first-party ones.
    Support for formats that are specific to a particular game would best
    belong in a separate Python library instead.

    That said, certain parts of ndspy (such as its support for ROM files and
    raw texture data) have to do with the console's hardware rather than its
    software, and thus should be relevant to most or all games.


<a name="installation"></a>
Installation
------------

ndspy requires Python 3.6 or newer to run. CPython (the reference
implementation of Python) and PyPy are both supported. Python 2, though, is not
supported at all.

The easiest way to get the latest stable release of ndspy is through PyPI using
pip.

pip is a command-line application, so you'll need to use the Windows command
prompt or bash to do this. The exact command you need to enter depends on your
operating system and the settings you chose when you installed Python. One of
the following possibilities will probably work for you, though:

    pip install ndspy

    python3 -m pip install ndspy

    py -3 -m pip install ndspy

If you want the very latest version of ndspy including features and bugfixes
not yet in any official release, you can also download the code from the
[GitHub repository](https://github.com/RoadrunnerWMC/ndspy) and install it
manually.


Documentation
-------------

[ndspy's documentation is hosted on Read the
Docs](https://ndspy.readthedocs.io/en/latest/index.html), and the documentation
source code can be found in the ``docs/`` folder in this repository. In
addition to the [API
reference](https://ndspy.readthedocs.io/en/latest/api/index.html), there are
also
[examples](https://ndspy.readthedocs.io/en/latest/index.html#a-few-examples-of-ndspy-in-action)
and [tutorials](https://ndspy.readthedocs.io/en/latest/tutorials/index.html) to
help you out!


Support
-------

I spent a long time writing the documentation for ndspy, so first please
double-check that your question isn't already answered in the [API
reference](https://ndspy.readthedocs.io/en/latest/api/index.html) or
[Tutorials](https://ndspy.readthedocs.io/en/latest/tutorials/index.html)
sections in the documentation.

If that doesn't help, you can ask me (RoadrunnerWMC) your questions via [the
ndspy Discord server](https://discord.gg/RQhxAxw). I'll try to get back to
you as quickly as I can!

If you think you've found a bug in ndspy, please [file an issue on
GitHub](https://github.com/RoadrunnerWMC/ndspy/issues/new). Thanks!


Versioning
----------

ndspy follows [semantic versioning](https://semver.org/) to the best of my
ability. If a tool claims to work with ndspy 1.0.2, it should also work with
ndspy 1.2.0, but not necessarily 2.0.0. (Please note that not all of those
version numbers actually exist!)

Undocumented modules are considered exempt from semantic versioning, and are
subject to drastic changes at any time. This is also mentioned in the
[Undocumented
APIs](https://ndspy.readthedocs.io/en/latest/api/index.html#undocumented-apis)
section of the documentation.
