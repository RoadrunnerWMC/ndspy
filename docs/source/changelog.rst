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
========================

This page contains the full changelog for all ndspy versions. All old versions
can be downloaded from the `Releases page on GitHub
<https://github.com/RoadrunnerWMC/ndspy/releases>`_.

.. contents:: :local:

1.0.0
-----

First release! The API has changed a lot in the weeks prior to this release, so
if you find yourself in possession of any code written for pre-1.0.0 ndspy,
you'll probably need to make adjustments.

.. note::

    This release had to be removed from PyPI due to a bug fixed in 1.0.1. If
    you really must have it for some reason, you can find it `on GitHub
    <https://github.com/RoadrunnerWMC/ndspy/releases/tag/v1.0.0>`_.

1.0.1
-----

Fixed an issue that caused pip to erroneously attempt to install on unsupported
versions of Python, instead of giving the correct error message.

2.0.0
-----

*   Updated the :py:mod:`ndspy.soundBank` API to reflect the new discovery that
    note definition type values are defined for all instrument types, not just
    single-note instruments. (Thanks, Gota7!) This is a backwards-incompatible
    change, hence the major version number bump.
*   Fixed some bugs in :py:mod:`ndspy.soundBank` and
    :py:mod:`ndspy.soundSequence` that caused crashes in some situations. If
    your code didn't crash on 1.0.x, this doesn't affect you.
*   Added :py:data:`ndspy.VERSION`.
*   Added this changelog page to the documentation.
