import argparse
import os, os.path

import ndspy.narc

import _common


# This is pretty unfinished at the moment.


def main():
    """
    Main function for NARC Tool.
    """

    parser = argparse.ArgumentParser(
        description='NARC Tool: Extract or pack NARC archives.')

    parser.add_argument('infile',
                        help='the file to be extracted, or the directory to be packed')
    parser.add_argument('outfile',
                        nargs='?', # https://stackoverflow.com/a/4480202
                        help='the output filename or directory name')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--extract',
                       action='store_true',
                       help='extract the archive'
                            " (don't try to guess whether to pack or extract)")
    group.add_argument('-p', '--pack',
                       action='store_true',
                       help='pack a new archive'
                            " (don't try to guess whether to pack or extract)")

    parser.add_argument('-l', '--lowlevel',
                        action='store_true',
                        help='if this is specified, the NARC will be '
                             ' extracted in a lower-level way that'
                             ' allows for better manual control of file'
                             ' IDs')

    args = parser.parse_args()

    if args.extract:
        shouldExtract = True
    elif args.pack:
        shouldExtract = False
    else:
        # Extract if it's a file, pack if it's a folder. :P
        if os.path.isfile(args.infile):
            shouldExtract = True
        elif os.path.isdir(args.infile):
            shouldExtract = False
        else:
            raise TypeError('Input file/folder is neither a file nor a folder.')

    outfile = args.outfile
    if outfile is None:
        outfile = args.infile + ('.dir' if shouldExtract else '.narc')

    convType = 'Extracting' if shouldExtract else 'Packing'
    lowlevelMsg = '(low-level representation)' if args.lowlevel else ''
    print(f'{convType} {args.infile} to {outfile} {lowlevelMsg}...')

    if shouldExtract:
        with open(args.infile, 'rb') as f:
            ind = f.read()
        filenames, files = ndspy.narc.load(ind)

        if args.lowlevel:
            fnt = _common.fntToJson(filenames)
            with open(os.path.join(outfile, 'filenames.json'),
                      'w', encoding='utf-8') as f:
                f.write(fnt)

            for i, filedata in enumerate(files):
                internalFn = filenames[i].split('/')[-1]
                extractFn = f'file_{i:0>4}_{internalFn}'

                with open(os.path.join(outfile, extractFn), 'wb') as f:
                    f.write(filedata)

        else: # not low-level
            ...

    else: # should unpack

        if args.lowlevel:

            ...

        else: # not low-level

            ...

        outd = ndspy.narc.save(filenames, files)
        with open(outfile, 'wb') as f:
            f.write(outd)

    print('Done.')


if __name__ == '__main__':
    main()
