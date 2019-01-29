import pathlib

testFilesPath = pathlib.Path('../test_files').resolve()

nsmbRomPath = testFilesPath / 'roms' / 'nsmb.nds'
haveNSMB = nsmbRomPath.is_file()
