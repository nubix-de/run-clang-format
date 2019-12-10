#!/usr/bin/env python
"""A wrapper script around clang-format, suitable for linting multiple files
and to use for continuous integration.

This is an alternative API for the clang-format command line.
It runs over multiple files and directories in parallel.
A diff output is produced and a sensible exit code is returned.

"""

import difflib
import sys


def main():
    fromlines = """I need to buy apples.
I need to run the laundry.
I need to wash the car.
I need to get the car detailed.
bla
if (foo) bar;
blub
function bazz() {
    foo;
    bla bla
}
""".splitlines(True)

    tolines = """I need to buy apples.
I need to do the laundry.
I need to wash the car.
I need to get the dog detailed.
bla
if (foo) {
    bar;
}
blub
function bazz () {
    foo;
    bla bla
}
""".splitlines(True)

    sm = difflib.SequenceMatcher(None, fromlines, tolines)

    for block in sm.get_matching_blocks():
        print("a[%d] and b[%d] match for %d elements" % block)

    for group in sm.get_grouped_opcodes(0):
        print("%6s a[%d:%d] b[%d:%d]" % group)


if __name__ == '__main__':
    sys.exit(main())
