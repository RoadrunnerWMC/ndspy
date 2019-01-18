
import ndspy.soundBank
import ndspy.soundWaveArchive


# This is ridiculously unfinished, obviously.


class SF2:
    """
    A class representing a SF2 soundfont.
    """

    def save(self):
        """
        Save this soundfont to a bytes object.
        """
        return b''



def convertToSF2(sbnk, swars):
    """
    Return a SF2 instance that closely matches the given SBNK using the
    given SWARs.
    """
    sf2 = SF2()
    return sf2



def main():
    with open('HGSS.sbnk', 'rb') as f:
        sbnkD = f.read()
    with open('HGSS.swar', 'rb') as f:
        swarD = f.read()

    sbnk = ndspy.soundBank.SBNK(sbnkD)
    sbnk.waveArchiveIDs = [0]
    swar = ndspy.soundWaveArchive.SWAR(swarD)

    sf2 = convertToSF2(sbnk, [swar])
    sf2D = sf2.save()
    with open('HGSS-ndspy.sf2', 'wb') as f:
        f.write(sf2D)


main()