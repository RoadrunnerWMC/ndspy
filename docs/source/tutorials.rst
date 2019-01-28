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

Tutorials
=========

This section contains tutorials to help you learn how to use ndspy!

I suggest starting with :doc:`tutorial00-gettingStarted` to ensure that you've
installed ndspy correctly and know how to run the correct copy of Python. After
that, you should try :doc:`tutorial01-editingRom`, which is intended to be a
relatively gentle introduction to basic ndspy usage. Once you've completed both
of those, you can pretty much jump around to whatever tutorials interest you.

Some familiarity with Python is assumed; however, we won't be using any
particularly advanced syntax [1]_, so it's OK if you're not too good at it yet.

These tutorials use *New Super Mario Bros.* as the example game, because it's
popular and it's what I'm most familiar with. However, ndspy should work with
any games that use file formats it supports.

.. [1]

    ``with`` blocks for opening files could be considered an exception;
    however, you don't really need to understand how they work in order to use
    them.

.. toctree::
    :maxdepth: 1
    :caption: Subpages

    tutorial00-gettingStarted
    tutorial01-editingRom
    tutorial02-editingNarc


.. todo::

    *   Exporting and importing within a NARC: show how to do it with a loose
        NARC as well as within a ROM.

    *   Messing with ARM9: change the value at 0xADDR to VALUE. Basically
        manual Magigoomba replaces. (Maybe also mention that you can do this
        with MG.)

    *   Messing with overlays: same as previous, but with overlays.

    *   Exporting and importing to/from SDAT: show how to save things out of an
        SDAT and import them back in. Include an example of exporting SWAVs
        from a SWAR.

    *   Importing a music track from one game into another: involves setting
        bank IDs and stuff. Also show how sequences can share banks and explain
        why you can't necessarily add new banks directly.

    *   Messing with a sound effect (very basic): swap a SWAV for another one
        -- as discussed on Discord.

    *   Messing with a sound effect (basic): change the 1-UP tune (maybe to the
        SMM 1UP-but-it-doesn't-count tune?).

    *   Messing with a sound effect (intermediate): replace something with a
        single NSMBW WAV. Should involve deleting some sequence events. After
        showing how to do it manually, show how it can be done using
        extras.soundEffect.

    *   Messing with a sound effect (advanced): insert the NSMBW powerup SFX,
        which has two notes and plays at two different pitches! Good place to
        use a regional instrument.

    *   Compressing/decompressing with LZ10.

    *   Editing BMG messages.
