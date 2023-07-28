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

Changelog
=========

This page contains the full changelog for all ndspy versions. All old versions
can be downloaded from the `Releases page on GitHub
<https://github.com/RoadrunnerWMC/ndspy/releases>`_.

.. contents:: :local:


4.1.0 (July 28, 2023)
---------------------
*   Replaced the `crcmod` dependency with a pure-Python CRC16 implementation in
    ndspy itself.
*   Fixed a bug in the undocumented :py:mod:`ndspy.graphics2D` module.
*   A few documentation improvements.


4.0.0 (Mar. 15, 2022)
---------------------

*   Many bugfixes. Thank you to everyone who reported bugs!
*   The :py:mod:`ndspy.codeCompression` and :py:mod:`ndspy.lz10` now have CLIs.
    They also gained convenience functions for compressing and decompressing
    to/from files rather than :py:class:`bytes` objects.
*   :py:class:`ndspy.bmg.BMG` now calls encoding value 1 ``'cp1252'`` rather
    than ``'latin-1'``; the latter was just a guess on my part. It also gained
    a new read-only attribute :py:class:`ndspy.bmg.BMG.fullEncoding` that is
    useful for manually decoding BMG strings, in case you need to do that for
    some reason.
*   :py:attr:`ndspy.rom.NintendoDSRom.iconBanner` now supports all versions
    of icon/banner data, not just the first version. The ``ICON_BANNER_LEN``
    constant has been removed, since it is not actually meaningful (different
    versions have different lengths).
*   :py:class:`ndspy.Processor` is now an :py:class:`enum.IntEnum`, rather than
    just an :py:class:`enum.Enum`.
*   Assertions now have messages indicating what went wrong.
*   The :py:mod:`ndspy` and :py:mod:`ndspy.bmg` modules now have unit tests.
*   Changes pertaining to undocumented modules:

    *    :py:mod:`ndspy.color`'s API has been redesigned. However, this may be
         reverted or redesigned again before the module is stabilized.
    *    Almost all :py:class:`ndspy.texture.TextureFormat` enum members were
         renamed.
    *    :py:mod:`ndspy.graphics2D` got further API improvements.
    *    :py:mod:`ndspy.extras.music` now automatically parses unparsed
         *SSEQ*\s.


3.0.0 (Feb. 10, 2019)
---------------------

*   Completely redesigned :py:mod:`ndspy.narc`'s API in order to add
    compatibility with *New Super Mario Bros.* This is a very
    backwards-incompatible change, and any code using the module definitely
    needs to be updated.
*   Medium-sized changes to :py:mod:`ndspy.bmg`'s API in order to add
    compatibility with... pretty much every game except *The Legend of Zelda:
    Phantom Hourglass* and *The Legend of Zelda: Spirit Tracks.* This is a
    pretty important change, of course, but it's also backwards-incompatible.
    Depending on what parts of the module your code uses, though, your code
    might still run correctly without any changes.
*   Converted the names of
    :py:class:`ndspy.soundSequence.MonoPolySequenceEvent.Value` and
    :py:class:`ndspy.soundSequence.VibratoTypeSequenceEvent.Value` members to
    upper-case, since that's the recommended style for enum members now. This
    is backward-incompatible, but only if your code uses these enums.
*   Added the first two tutorials to the documentation, and added example code
    for certain modules.
*   Reorganized the folder structure of the documentation. This makes most
    previous documentation links invalid, unfortunately, but the reorganization
    was done with an eye toward avoiding this having to happen again in the
    future.
*   Changes pertaining to undocumented modules:

    *    :py:mod:`ndspy.bnbl` and :py:mod:`ndspy.bncl` were added
    *    :py:mod:`ndspy.graphics2D` got some API improvements
    *    Swapped the interpretation of alpha values in :py:mod:`ndspy.color`
    *    Added the ability to render textures with :py:mod:`ndspy.texture`


2.0.0 (Jan. 23, 2019)
---------------------

*   Updated the :py:mod:`ndspy.soundBank` API to reflect the new discovery that
    note definition type values are defined for all instrument types, not just
    single-note instruments. (Thanks, Gota7!) This is a backwards-incompatible
    change, hence the major version number bump.
*   Fixed some bugs in :py:mod:`ndspy.soundBank` and
    :py:mod:`ndspy.soundSequence` that caused crashes in some situations. If
    your code didn't crash on 1.0.x, this doesn't affect you.
*   Added :py:data:`ndspy.VERSION`.
*   Added this changelog page to the documentation.


1.0.1 (Jan. 18, 2019)
---------------------

Fixed an issue that caused pip to erroneously attempt to install on unsupported
versions of Python, instead of giving the correct error message.


1.0.0 (Jan. 18, 2019)
---------------------

First release! The API has changed a lot in the weeks prior to this release, so
if you find yourself in possession of any code written for pre-1.0.0 ndspy,
you'll probably need to make adjustments.

.. note::

    This release had to be removed from PyPI due to a bug fixed in 1.0.1. If
    you really must have it for some reason, you can find it `on GitHub
    <https://github.com/RoadrunnerWMC/ndspy/releases/tag/v1.0.0>`_.
