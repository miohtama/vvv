#!/usr/bin/env python
"""
Orignal recipe by http://code.activestate.com/recipes/498179-expand_tabspy-expand-tabs-in-files-in-place/
"""
import fileinput, optparse, sys

# E1103: 35,8:run: Instance of 'int' has no 'write' member (but some types could not be inferred)
# pylint: disable=E1103

def run():

    # Command-line parser
    parser = optparse.OptionParser(
            usage="""
    %prog [options] [files]
    Expand tab to spaces, printing to the standard output by default.
    When no files are given, read from the standard input.

    Examples:
     expand in one file
        % expand_tabs.py -t 4 file.txt

     expand tabs in Python source files
        % find . -name "*.py" | xargs expand_tabs.py -it 4
    """.strip(),
            formatter=optparse.IndentedHelpFormatter(max_help_position=30)
        )
    parser.add_option("-t", "--tabsize", type="int", metavar="SIZE")
    parser.add_option("-i", "--inplace", action="store_true", help="change the files in-place (don't print)")
    parser.add_option("-b", "--backupext", default="", metavar="EXT", help="backup extension to use (default: no backup)")

    options, args = parser.parse_args()
    if options.tabsize is None:
        parser.error("tab size not specified")

    # Do the work
    for line in fileinput.input(files=args, inplace=options.inplace, backup=options.backupext):
        sys.stdout.write( line.expandtabs(options.tabsize) )


if __name__ == "__main__":
    run()