
import os, os.path
import shutil

import ndspy.soundArchive


def testSDAT(sdatsFolder):
    """
    Open each SDAT in a folder full of them. Parse each one with ndspy,
    and immediately resave (to a subfolder named "out"). Compare each
    output with the original data, and declare the test a failure if any
    of the output files differ in any way from the input file.
    """
    # Prepare the output directory
    outDir = os.path.join(sdatsFolder, 'out')
    if os.path.isdir(outDir):
        shutil.rmtree(outDir)
    os.mkdir(outDir)

    success = True

    # Iterate over each SDAT
    for fn in sorted(os.listdir(sdatsFolder)):
        if not fn.endswith('.sdat'): continue
        name = fn[:-5]
        full = os.path.join(sdatsFolder, fn)

        # Open
        with open(full, 'rb') as f:
            sdatD = f.read()
        sdat = ndspy.soundArchive.SDAT(sdatD)

        # Save
        sdatD2 = sdat.save()
        with open(os.path.join(outDir, name + '_out.sdat'), 'wb') as f:
            f.write(sdatD2)

        # Check for correctness
        if sdatD == sdatD2:
            result = 'good'
        else:
            # Here, you can define any expected failures.
            if name == "ace_attorney_investigations_miles_edgeworth_2_prosecutor's_path":
                result = 'wontfix: Fangame; SWAR padding is insane'
            else:
                result = 'BAD'
                success = False

        # Print the outcome of this SDAT with nice formatting
        line = fn + ' '
        while len(line) < 70: line += '.'
        line += ' ' + result
        print(line)

    return success


def main():
    success = testSDAT('/home/user/zed/Music/SDATS/')
    if not success:
        print('TEST FAILURE')


main()