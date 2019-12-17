#!/usr/bin/env python
"""A wrapper script around clang-format, suitable for linting multiple files
and to use for continuous integration.

This is an alternative API for the clang-format command line.
It runs over multiple files and directories in parallel.
A diff output is produced and a sensible exit code is returned.

"""

import difflib
import sys
import json

import xml.etree.cElementTree as ET


def main():
    a = """I need to buy apples.
I need to run the laundry.
qwerqwer
I need to wash the car.


I need to get the car detailed.
bla
if (foo) bar;
blub
function bazz() {
    foo;
    bla bla
}
I need to run the laundry.
Bla Blub
I need to wash the car.
""".splitlines(True)

    b = """I need to buy apples.
I need to do the laundry.
I need to wash the car.
I need to get the dog detailed.
bla
if (foo) {
    bar;
}
blub
qwerqwer
function bazz () {
    foo;
    bla bla
}
I need to run the laundry.
I need to wash the car.
asdfasdf
""".splitlines(True)

    print("A:")
    for idx, val in enumerate(a):
        sys.stdout.write('{:2d}: {!s}'.format(idx, val))

    print("")
    print("B:")
    for idx, val in enumerate(b):
        sys.stdout.write('{:2d}: {!s}'.format(idx, val))

    s = difflib.SequenceMatcher(None, a, b)

    print("")
    print("get_opcodes")
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        # if tag != 'equal':
        if True:
            print('{:7}   a[{:3d}:{:3d}] --> b[{:3d}:{:3d}]   {:>40} --> {!s}'.format(
                tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))

    #    print("")
    #    print("get_grouped_opcodes")
    #    for group in s.get_grouped_opcodes(0):
    #        for tag, i1, i2, j1, j2 in group:
    #            if tag != 'equal':
    #                print('{:7}   a[{:3d}:{:3d}] --> b[{:3d}:{:3d}]   {:>40} --> {!s}'.format(
    #                    tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))
    #                # a[i1:i2]

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != 'equal':
            print('{:7}   a[{:3d}:{:3d}] --> b[{:3d}:{:3d}]   {:>40} --> {!s}'.format(
                tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))

    print("")
    print("xml-export")

    root = ET.Element("root")
    doc = ET.SubElement(root, "doc", fileName='foo.c')

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != 'equal':
            print('{:7}   a[{:3d}:{:3d}] --> b[{:3d}:{:3d}]   {:>40} --> {!s}'.format(
                tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))

            ET.SubElement(doc, tag, lineStart=str(i1), lineEnd=str(i2))

    tree = ET.ElementTree(root)
    tree.write(sys.stdout)
    print("")

    print("")
    print("json-export")

    root = {}
    doc = root['issues'] = []


    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != 'equal':
            doc.append({
                'fileName': 'foo.c',
                'lineRanges': [
                    {
                        "start": str(i1),
                        "end": str(i2)
                    }
                ]
            })

    json.dump(root, sys.stdout)
    print("")


if __name__ == '__main__':
    sys.exit(main())
