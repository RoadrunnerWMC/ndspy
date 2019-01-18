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


import struct

from . import _common
from . import color


HavePIL = True
try:
    import PIL.Image
except ImportError:
    HavePIL = False


def loadPalette(data):
    """
    Convert binary data to a list of (r, g, b, a) color tuples.
    This is the inverse of savePalette().
    """
    colors = []
    colorVals = struct.unpack_from(f'<{len(data) // 2}H', data)
    colors = [color.LUT_UNPACKED_255[c] for c in colorVals]
    return colors


def savePalette(colors):
    """
    Convert a list of (r, g, b, a) color tuples to binary data.
    This is the inverse of loadPalette().
    """
    colorVals = [color.pack255(r, g, b, a) for (r, g, b, a) in colors]
    return struct.pack(f'<{len(colors)}H', *colorVals)


class ImageTile:
    """
    A class that represents a single image tile.
    """
    data = None
    is4bpp = False

    def __init__(self, data, is4bpp=False):
        """
        data should be bytes or bytearray
        """
        self.data = data
        self.is4bpp = is4bpp


    def render(self, colors, paletteNum=0):
        """
        Given a list of colors and the desired palette number to use, 
        render this ImageTile as a PIL Image.
        colors should be a list of (r, g, b, a) tuples.
        """
        if not HavePIL:
            raise RuntimeError('PIL is not installed, so ndspy cannot render ImageTiles.')

        cs = paletteNum * (16 if self.is4bpp else 256)
        img = PIL.Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        for y in range(8):
            if self.is4bpp:
                for x in range(0, 8, 2):
                    col12 = self.data[y * 4 + x // 2]
                    col1, col2 = col12 & 0xF, col12 >> 4
                    if col1:
                        img.putpixel((x, y), colors[cs + col1])
                    if col2:
                        img.putpixel((x+1, y), colors[cs + col2])
            else:
                for x in range(8):
                    col = self.data[y * 8 + x]
                    if col:
                        img.putpixel((x, y), colors[cs + col])

        return img


def loadImageTiles(data, is4bpp=False):
    """
    Convert binary data to a list of ImageTiles.
    This is the inverse of saveImageTiles().
    """
    bytesPerTile = 32 if is4bpp else 64
    tileCount = len(data) // bytesPerTile

    tiles = []
    for i in range(tileCount):
        start = i * bytesPerTile
        tiles.append(ImageTile(data[start : start+bytesPerTile], is4bpp))

    return tiles


def saveImageTiles(tiles):
    """
    Convert a list of ImageTiles to binary data.
    This is the inverse of loadImageTiles().
    """
    return b''.join(t.data for t in tiles)


class TilemapTile:
    """
    A class representing a single tilemap tile
    """
    tileNum = 0
    hFlip = False
    vFlip = False
    paletteNum = 0

    def __init__(self, value=0):
        """
        Initialize the TilemapTile from a raw 16-bit data value.
        """
        self.value = value


    @classmethod
    def fromParameters(cls, tileNum, hFlip=False, vFlip=False, paletteNum=0):
        """
        Create a new TilemapTile with the parameters given.
        """
        self = cls()
        self.tileNum = tileNum
        self.hFlip = hFlip
        self.vFlip = vFlip
        self.paletteNum = paletteNum
        return self


    @property
    def value(self):
        """
        This tile's 16-bit data value.
        """
        v = 0
        v |= self.tileNum & 0x3FF
        if self.hFlip: v |= 0x400
        if self.vFlip: v |= 0x800
        v |= (self.paletteNum & 0xF) << 12
        return v

    @value.setter
    def value(self, v):
        self.tileNum = v & 0x3FF
        self.hFlip = bool(v & 0x400)
        self.vFlip = bool(v & 0x800)
        self.paletteNum = (v >> 12) & 0xF


    def renderSingle(self, imageTile, colors):
        """
        Given an image tile and a list of colors, render this
        TilemapTile as a PIL Image.
        imageTile should be an ImageTile.
        colors should be a list of (r, g, b, a) tuples.
        """
        if not HavePIL:
            raise RuntimeError('PIL is not installed, so ndspy cannot render TilemapTiles.')

        img = imageTile.render(colors, tile.paletteNum)
        if self.hFlip:
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        if self.vFlip:
            img = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        return img


    def render(self, imageTiles, colors, tileNumOffset=0):
        """
        Given lists of image tiles and colors, render this TilemapTile
        as a PIL Image.
        imageTiles should be a list of, well, ImageTiles.
        colors should be a list of (r, g, b, a) tuples.
        """
        if self.tileNum < tileNumOffset:
            raise ValueError(f'TilemapTile.tileNum < tileNumOffset ({self.tileNum} < {tileNumOffset})')
        return self.renderSingle(imageTiles[self.tileNum - tileNumOffset],
                                 colors)


def loadTilemapTiles(data):
    """
    Convert binary data to a list of TilemapTiles.
    This is the inverse of saveTilemapTiles().
    """
    tiles = []
    for i in range(0, len(data), 2):
        t, = struct.unpack_from('<H', data, i)
        tiles.append(TilemapTile(t))
    return tiles


def saveTilemapTiles(tiles):
    """
    Convert a list of TilemapTiles to binary data.
    This is the inverse of loadTilemapTiles().
    """
    return b''.join(struct.pack('<H', t.value) for t in tiles)


def renderImageTiles(tiles, colors, paletteNum=0, width=32):
    """
    Given a list of ImageTiles, a list of colors, a desired palette
    ID to render with, render all the tiles as a single image.
    The width of the image defaults to 32 tiles, but can be adjusted.
    """
    if not HavePIL:
        raise RuntimeError('PIL is not installed, so ndspy cannot render ImageTiles.')

    height, remainder = divmod(len(tileImages), width)
    if remainder: height += 1

    img = PIL.Image.new('RGBA', (8 * width, 8 * height), (0, 0, 0, 0))

    tileIter = iter(tiles)
    for y in range(height):
        for x in range(width):
            tileImg = next(tileIter).render(colors, paletteNum)
            img.paste(tileImg, (x * 8, y * 8))

    return img


def renderTilemap(tilemapTiles, imageTiles, colors, width, tileNumOffset=0):
    """
    Given a list of TilemapTiles, a list of ImageTiles, a list of
    colors, render the tilemap to an image. The tilemap's width must
    also be specified.
    """
    height, remainder = divmod(len(tilemapTiles), width)
    if remainder: height += 1

    img = PIL.Image.new('RGBA', (8 * width, 8 * height), (0, 0, 0, 0))

    tilemapIter = iter(tilemapTiles)
    for y in range(height):
        for x in range(width):
            tileImg = next(tilemapIter).render(imageTiles, colors, tileNumOffset)
            img.paste(tileImg, (x * 8, y * 8))

    return img


def tileAt(tiles, x, y, w=32):
    """
    Convenience function: return the tile at (x, y) in the tile list
    given, assuming a row width of `w` (32 by default).
    """
    return tiles[y * w + x]


def putTile(tiles, x, y, t, w=32):
    """
    Convenience function: replace the tile at (x, y) in the tile list
    given with `t`, assuming a row width of `w` (32 by default).
    If (x, y) is not in the tile list, nothing happens.
    """
    if x >= w or y >= w: return
    if x < 0 or y < 0: return
    try:
        tiles[y * w + x] = t
    except IndexError: pass
