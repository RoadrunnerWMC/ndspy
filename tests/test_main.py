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
Unit tests for ndspy.__init__.
"""


import ndspy
import pytest


def test_VERSION():
    """
    Test the ndspy.VERSION namedtuple
    """
    assert ndspy.VERSION.major == ndspy.VERSION[0] >= 0
    assert ndspy.VERSION.minor == ndspy.VERSION[1] >= 0
    assert ndspy.VERSION.patch == ndspy.VERSION[2] >= 0
    assert type(ndspy.VERSION).__name__ == 'ndspy.version'


def test_Processor():
    """
    Test the ndspy.Processor enum
    """
    assert ndspy.Processor.ARM9 == 9
    assert ndspy.Processor.ARM7 == 7


def test_WaveType():
    """
    Test the ndspy.WaveType enum
    """
    assert ndspy.WaveType.PCM8 == 0
    assert ndspy.WaveType.PCM16 == 1
    assert ndspy.WaveType.ADPCM == 2


def test_findInNamedList():
    """
    Test ndspy.findInNamedList()
    """
    # Normal use
    assert ndspy.findInNamedList([(1, 2), (3, 4), (5, 6)], 3) == 4

    # Duplicate names (should find first one)
    assert ndspy.findInNamedList([(1, 2), (3, 4), (1, 6)], 1) == 2

    # Missing name
    with pytest.raises(KeyError):
        ndspy.findInNamedList([(1, 2), (3, 4), (5, 6)], 2)


def test_indexInNamedList():
    """
    Test ndspy.indexInNamedList()
    """
    # Normal use
    assert ndspy.indexInNamedList([(1, 2), (3, 4), (5, 6)], 3) == 1

    # Duplicate names (should find first one)
    assert ndspy.indexInNamedList([(1, 2), (3, 4), (1, 6)], 1) == 0

    # Missing name
    with pytest.raises(KeyError):
        ndspy.indexInNamedList([(1, 2), (3, 4), (5, 6)], 2)


def test_setInNamedList():
    """
    Test ndspy.setInNamedList()
    """
    # Normal use
    L = [(1, 2), (3, 4), (5, 6)]
    ndspy.setInNamedList(L, 3, 7)
    assert L == [(1, 2), (3, 7), (5, 6)]

    # Duplicate names (should find first one)
    L = [(1, 2), (3, 4), (1, 6)]
    ndspy.setInNamedList(L, 1, 7)
    assert L == [(1, 7), (3, 4), (1, 6)]

    # Missing name
    with pytest.raises(KeyError):
        L = [(1, 2), (3, 4), (5, 6)]
        ndspy.setInNamedList(L, 2, 7)
