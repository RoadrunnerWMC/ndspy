import argparse
import os, os.path

import ndspy.fnt
import ndspy.narc
import ndspy.rom

import _common


def main():
    """
    Main function for FNT Tool.
    """

    parser = argparse.ArgumentParser(
        description='FNT Tool: Extract or insert filename tables to or'
                    ' from ROM or NARC files, either as binary or JSON'
                    ' files.')

    parser.add_argument('infile',
                        help='the file to be converted')
    parser.add_argument('outfile',
                        help='the output filename')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ib', '--input_bin',
                       action='store_true',
                       help='the input file is a raw filename table file')
    group.add_argument('-ij', '--input_json',
                       action='store_true',
                       help='the input file is a JSON file')
    group.add_argument('-ir', '--input_rom',
                       action='store_true',
                       help='the input file is a ROM')
    group.add_argument('-in', '--input_narc',
                       action='store_true',
                       help='the input file is a NARC file')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ob', '--output_bin',
                       action='store_true',
                       help='save the filename table to a raw filename'
                            ' table file')
    group.add_argument('-oj', '--output_json',
                       action='store_true',
                       help='save the filename table to a JSON file')
    group.add_argument('-or', '--output_rom',
                       action='store_true',
                       help='insert the filename table into a ROM'
                            ' (the ROM file must already exist)')
    group.add_argument('-on', '--output_narc',
                       action='store_true',
                       help='insert the filename table into a NARC file'
                            ' (the NARC file must already exist)')

    args = parser.parse_args()

    # Make sure that outfile exists if we're going to insert
    if (args.output_rom or args.output_narc) and not os.path.exists(args.outfile):
        raise ValueError('To use -or or -on, the output file must already exist!')

    # Open the input file
    with open(args.infile, 'rb') as f:
        ind = f.read()

    # Load the filename table from it
    print(f'Loading filenames from {args.infile}...')
    fnt = None
    if args.input_bin:
        fnt = ndspy.fnt.load(ind)
    elif args.input_json:
        fnt = _common.jsonToFnt(ind.decode('utf-8'))
    elif args.input_rom:
        fnt = ndspy.rom.NintendoDSRom(ind).filenames
    elif args.input_narc:
        fnt, _ = ndspy.narc.load(ind)

    assert fnt is not None

    # Open the output file, if it exists
    existing = None
    if os.path.isfile(args.outfile):
        with open(args.outfile, 'rb') as f:
            existing = f.read()

    # Create the output data in the requested format
    if args.output_rom or args.output_narc:
        print(f'Inserting filenames into {args.outfile}...')
    else:
        print(f'Saving filenames to {args.outfile}...')
    outd = None
    if args.output_bin:
        outd = ndspy.fnt.save(fnt)
    elif args.output_json:
        outd = _common.fntToJson(fnt).encode('utf-8')
    elif args.output_rom:
        rom = ndspy.rom.NintendoDSRom(existing)
        rom.filenames = fnt
        outd = rom.save()
    elif args.output_narc:
        _, files = ndspy.narc.load(existing)
        outd = ndspy.narc.save(fnt, files)

    assert outd is not None

    # Save it
    with open(args.outfile, 'wb') as f:
        f.write(outd)

    print('Done.')


if __name__ == '__main__':
    main()
