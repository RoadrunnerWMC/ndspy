ndspy
=====

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
platforms Python supports.

Interested? Read on to see some examples, or check the [API
Reference](https://ndspy.readthedocs.io/en/latest/api.html) to see the
documentation for a specific module. When you're ready to install, head over to
the [Installation](#installation) section!



A few examples of ndspy in action
---------------------------------

Create a *BMG* file containing message strings:

```python
>>> import ndspy.bmg
>>> message1 = ndspy.bmg.Message(0, ['Open your eyes...'])
>>> message2 = ndspy.bmg.Message(0, ['Wake up, Link...'])
>>> bmg = ndspy.bmg.BMG.fromMessages([message1, message2])
>>> bmg.save()
b'MESGbmg1\xa0\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00INF1 \x00\x00\x00\x02\x00\x08\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00&\x00\x00\x00\x00\x00\x00\x00DAT1`\x00\x00\x00\x00\x00O\x00p\x00e\x00n\x00 \x00y\x00o\x00u\x00r\x00 \x00e\x00y\x00e\x00s\x00.\x00.\x00.\x00\x00\x00W\x00a\x00k\x00e\x00 \x00u\x00p\x00,\x00 \x00L\x00i\x00n\x00k\x00.\x00.\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
>>> game = ndspy.rom.NintendoDSRom.fromFile('game.nds')
>>> for i, file in enumerate(game.files):
...     if file.startswith(b'BMD0'):
...         print(game.filenames[i] + ' is a NSBMD model')
...
demo/end_kp.nsbmd is a NSBMD model
demo/staffroll.nsbmd is a NSBMD model
demo/staffroll_back.nsbmd is a NSBMD model
enemy/A_jiku.nsbmd is a NSBMD model
enemy/all_goal_flag.nsbmd is a NSBMD model
[snip]
map/world7.nsbmd is a NSBMD model
map/world8.nsbmd is a NSBMD model
>>>
```


<a name="installation"></a>
Installation
------------

ndspy requires Python 3.6 or newer to run. Python 2 is not supported at all.

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
manually. Note that [crcmod](https://pypi.org/project/crcmod/) is a required
dependency.


Documentation
-------------

[ndspy's documentation is hosted on Read the
Docs](https://ndspy.readthedocs.io/en/latest/index.html), and the documentation
source code can be found in the ``docs/`` folder in this repository. In
addition to the [API
reference](https://ndspy.readthedocs.io/en/latest/api.html), there are also
[examples](https://ndspy.readthedocs.io/en/latest/index.html#a-few-examples-of-ndspy-in-action)
and [tutorials](https://ndspy.readthedocs.io/en/latest/tutorials.html) to help
you out!


Support
-------

I spent a long time writing the documentation for ndspy, so first please
double-check that your question isn't already answered in the [API
reference](https://ndspy.readthedocs.io/en/latest/api.html) or
[Tutorials](https://ndspy.readthedocs.io/en/latest/tutorials.html) sections in
the documentation.

If that doesn't help, you can ask me (RoadrunnerWMC) your questions via [the
ndspy Discord server](https://discord.gg/RQhxAxw). I'll try to get back to
you as quickly as I can!

If you think you've found a bug in ndspy, please [file an issue on
GitHub](https://github.com/RoadrunnerWMC/ndspy/issues/new). Thanks!


Versioning
----------

ndspy follows [semantic versioning](https://semver.org/) to the best of my
ability. If a tool claims to work with ndspy 1.0.2, it should also work with
ndspy 1.2.0, but not necessarily 2.0.0. (Please note that ndspy hasn't actually
reached these version numbers yet!)

Undocumented modules are considered exempt from semantic versioning, and are
subject to drastic changes at any time. This is also mentioned in the
[Undocumented
APIs](https://ndspy.readthedocs.io/en/latest/api.html#undocumented-apis)
section of the documentation.
