import argparse

import ndspy.lz10


def main():
    """
    Main function for LZ10 Tool.
    """

    parser = argparse.ArgumentParser(
        description='LZ10 Tool: Compress or decompress files with LZ10.')

    parser.add_argument('infile',
                        help='the file to be [de]compressed')
    parser.add_argument('outfile',
                        nargs='?', # https://stackoverflow.com/a/4480202
                        help='the output filename')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--compress',
                       action='store_true',
                       help='compress the file'
                            " (don't try to guess whether to compresss or decompress)")
    group.add_argument('-d', '--decompress',
                       action='store_true',
                       help='decompress the file'
                            " (don't try to guess whether to compresss or decompress)")

    args = parser.parse_args()

    with open(args.infile, 'rb') as f:
        ind = f.read()

    if args.compress:
        shouldCompress = True
    elif args.decompress:
        shouldCompress = False
    else:
        # LZ10-compressed files always start with 0x10.
        # This will turn up a few false positives, but it should be
        # a relatively good heuristic.
        shouldCompress = ind[0] != 0x10

    outfile = args.outfile
    if outfile is None:
        outfile = args.infile + ('.lz10' if shouldCompress else '.raw')

    convType = 'Compressing' if shouldCompress else 'Decompressing'
    print(f'{convType} {args.infile} to {outfile} ...')

    lz = ndspy.lz10
    outd = (lz.compress if shouldCompress else lz.decompress)(ind)

    with open(outfile, 'wb') as f:
        f.write(outd)

    print('Done.')


if __name__ == '__main__':
    main()
