import ndspy.soundArchive
import ndspy.soundSequence

import os, os.path

# This is a total mess currently. I'm just leaving the code here so that
# I can turn it into something useful eventually.


def midiAndSF2ToMP3(inMIDI, inSF2, outMP3):
    # https://wiki.archlinux.org/index.php/FluidSynth#How_to_convert_MIDI_to_MP3.2FOGG
    os.system(f'fluidsynth -l -T raw -F - "{inSF2}" "{inMIDI}" | twolame -b 256 -r - "{outMP3}"')


def makeScaleSSEQ(bankID, instrumentID):
    sseq = ndspy.soundSequence.SSEQ()
    sseq.events.append(ndspy.soundSequence.InstrumentSwitchSequenceEvent(bankID, instrumentID))
    for i in range(0x80):
        sseq.events.append(ndspy.soundSequence.NoteSequenceEvent(i, 127, 50))
    sseq.events.append(ndspy.soundSequence.EndTrackSequenceEvent())
    return sseq


def prepareSDAT(inFN, outFN):
    with open(inFN, 'rb') as f:
        sdatD = f.read()
    sdat = ndspy.soundArchive.SDAT(sdatD)

    swar = sdat.waveArchives[0][1]
    sbnks = {}
    for i, (name, sbnk) in enumerate(sdat.banks):
        if 0 in sbnk.waveArchiveIDs:
            sbnks[i] = sbnk

    temp = []
    for sbnkID, sbnk in sbnks.items():
        for instID, inst in enumerate(sbnk.instruments):
            temp.append(inst)
    print(len(temp))
    return

    sseqs = []
    for sbnkID, sbnk in sbnks.items():
        for instID, inst in enumerate(sbnk.instruments):
            if inst is None: continue
            sseq = makeScaleSSEQ(0, instID)
            sseq.bankID = sbnkID
            print(f'{len(sseqs)}: "{"%03d" % sbnkID}.{"%02d" % instID}.mp3",')
            sseqs.append((None, sseq))

    sdat.sequences = sseqs

    sdatD2 = sdat.save()
    with open(outFN, 'wb') as f:
        f.write(sdatD2)


def main():
    prepareSDAT('final_sound_data.sdat', 'final_sound_data_out.sdat')

main()
