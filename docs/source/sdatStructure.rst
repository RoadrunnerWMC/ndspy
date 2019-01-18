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

Appendix: SDAT Structure
========================

This page explains how the files within an *SDAT* sound archive file relate to
each other. There won't be anything specific to ndspy here, so if you already
know how *SDAT* files are organized, you can ignore this page.

.. contents:: :local:

Overview
--------

In most Nintendo DS games, a single *SDAT* file (often named *sound_data.sdat*
or similar) will contain all of the game's sound data: all music and sound
effects, in a single file. Some music is in the form of "streams" (similar to a
*mp3* or *wav* file), but usually, to save memory, most or all of it will be in
the form of "sequences" (similar to a `midi file
<https://en.wikipedia.org/wiki/MIDI>`_). The instruments used to play the
sequences contain streams for note sounds, and metadata. Sound effects are
always sequences, although they usually use unique "instruments" made just for
them, and are often only one note long.

*SDAT*\: overall container
--------------------------

An *SDAT* ("sound data") file contains many *SWAR*, *SBNK*, *SSEQ*, *SSAR*,
*Sequence player*, *STRM*, *Stream player*, and/or *Group* files. Some *SDAT*
files include filenames for the files they contain, but this isn't a
requirement; they are sometimes omitted to save space. Games generally refer to
files within an *SDAT* by their ID numbers, so missing filenames is only an
inconvenience.

You might wonder why an *SDAT* contains files that contain things, when the
*SDAT* could in theory simply contain the items itself. (For example, an *SDAT*
will usually contain many *SBNK* files, which each contain many instruments.)
It's structured this way so that games can easily load groups of related sounds
at the same time. For example, there's no point in loading the instruments for
the battle music if the game is currently displaying the main menu.

*SWAV*\: short stream
---------------------

An *SWAV* ("sound wave") file is a short mono audio clip that can optionally be
looped. This is usually a single note played by an instrument, or a sound
effect. Even though these contain the raw audio data for sound effects, games
never directly look for *SWAV*\s when they want to play a particular sound
effect. Instead, they'll reference sequence entries within *SSAR* files, which
play notes using instruments that use the appropriate *SWAV*\s.

These can usually only be found within *SWAR* files.

*SWAR*\: folder of *SWAV*\s
---------------------------

A *SWAR* ("sound wave archive") file is essentially a folder of *SWAV* files.
The files within are unnamed, and can only be referenced by number.

*SBNK* files use these.

*SBNK*\: folder of instruments
------------------------------

An *SBNK* ("sound bank") file is a set of instruments that can be used by a
sequence.

It can define up to four file IDs of *SWAR* files that contain the sound
"samples" that its instruments need. Instruments within the *SBNK* can refer to
a particular *SWAR* by specifying which of these file IDs to use (numbered
beginning at 0; that is, 0, 1, 2, or 3).

There are three types of instruments, and all of them make use of "note
definitions":

Note definition
+++++++++++++++

A *note definition* defines one note that an instrument can play. It includes
all of the following:

*   A *SWAR* number (specifically, an index (0-3) into the *SWAR* ID list in the
    *SBNK*), and the number of an *SWAV* within it.
*   Which note this is, as a number. Examples: 60 (middle C), 74 (high D), 46
    (low A♯).
*   Some technical parameters to fine-tune the sound: "attack rate", "decay
    rate", "sustain rate", "release rate" and "pan".

Even though a note definition only defines a single note (say, middle C), games
can (and do) use a single note definition to play a variety of notes. This is
done by playing the sample at a faster or slower sample rate to artificially
make it sound higher or lower. Games calculate the required sample rate for
this automatically; you never need to deal with the specifics of how that
works.

Single-note instrument
++++++++++++++++++++++

The simplest kind of instrument. This contains one note definition and nothing
else.

Remember, that doesn't mean that only one note can be played on this
instrument. The game can produce all other notes by playing the sample faster
or slower to change its pitch.

Range instrument
++++++++++++++++

Instruments of this type declare a range of note numbers (for example, 60
through 72), and contain one note definition for each number in that range. The
note numbers defined in the note definitions may not always match what you'd
expect them to be given their positions in the range.

Regional instrument
+++++++++++++++++++

This type of instrument declares up to eight non-overlapping "regions" that
together span the entire range of valid note pitches (0 through 127). Each
region gets one note definition, from which the game produces all other notes
in that region.

*SSEQ*\: sequenced music
------------------------

A *SSEQ* ("sound sequence") file is a single piece of sequenced music. It
includes:

*   the ID number of an *SBNK*
*   technical stuff: volume, "channel pressure", "polyphonic pressure", "play"
*   a list of events

Events are semantically similar to those of *midi* files. They're essentially
commands that explain how the song is to be played. They include notes and
rests, as well as directives to change instruments, to start multiple tracks
playing at once, to jump, to loop, and much more. Events can have parameters,
which vary per event type.

*SSAR*\: sequenced sound effects
--------------------------------

A *SSAR* ("sound sequence archive") file contains a set of sound effects. Each
sound effect includes all of the metadata of an *SSEQ*, and they all share a
single pool of events.

Sound effects sound different because they begin at different locations in the
event pool. They usually avoid overlapping with each other by using events that
end sequence execution. Similar sound effects, however, sometimes take
advantage of the shared event space by using jump events to share events with
each other. This can sometimes make it tricky to edit individual sound effects
without accidentally affecting others.

*Sequence player*\: limits for sequences
----------------------------------------

A *sequence player* defines the maximum number of sequences that can be played
at once, and the overall amount of memory that can be allocated at once to hold
sequence data. It also lists the hardware sound channels that may be used for
playing sequences, to avoid conflicts with any streams that may be playing at
the same time.

Some games use multiple sequence players at once. When they do, the maximum
number of sequences that can play concurrently will be small for each one, the
amount of memory to allocate will be set to zero (to be calculated at runtime
instead), and no allowed hardware channels will be listed (also to be
determined at runtime).

*STRM*\: multi-channel stream
-----------------------------

A *STRM* ("sound stream") is essentially a *SWAV* that supports multiple
channels. While *SWAV*\s are used for instrument sound samples, these are used
for full music tracks. They stand on their own and don't reference any other
files.

*Stream player*\: allowed channels for streams
----------------------------------------------

A *stream player* lists the hardware channels that *STRM*\s may play on. This
is needed to avoid conflicts with sequenced sounds that may be playing at the
same time.

For example, [6, 7] means that the first channel of the first stream to be
played should be played on hardware channel 6, and the next should be played on
7 (both zero-indexed). Attempts to play more than two *STRM* channels in this
example would fail.

*Group*\: group of items
------------------------

A *group* is a collection of IDs of items that exist elsewhere in the *SDAT*.
These items can be of different types. Games use these to group files together
that should be loaded at the same time. These are sometimes also known as
"sound sets."
