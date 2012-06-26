"""

    Add more globals declarations to .js files.

    To run this script

    - Install VVV and activate virtualenv http://miohtama.github.com/vvv/installation.html#installing-locally-using-virtualenv

"""

import plac
import re
import sys
import os
import tempfile
from shutil import move


def is_globals_line(line):
    line = line.strip()
    return line.startswith("/* global") or line.startswith("/*global")


def is_comment_line(line):
    line = line.strip()

    markers = ["/*", "*", "*/"]

    for m in markers:
        if line.startswith(m):
            return True


def generate_globals_line(line, jsglobals):
    """
    """

    parsed_globals = []

    bad_tokens = ["/*", "*/", "global"]

    if line:

        # http://stackoverflow.com/a/1059601/315168
        existing = re.split("\W+", line)

        for token in existing:
            token = token.strip()

            if token == "":
                continue

            if not token in bad_tokens:
                parsed_globals.append(token)

    for newglobal in jsglobals:
        if not newglobal in parsed_globals:
            parsed_globals.append(newglobal)

    # http://www.jslint.com/lint.html style

    return "/*global %s */" % ", ".join(parsed_globals)


def add_new_globals_after_comment(text, jsglobals):
    """
    Add globals line after the first comment in the file.
    """

    output = []

    in_start_comment = True

    for line in text.split("\n"):

        if in_start_comment and not is_comment_line(line):
            # Inject globals
            globals_line = generate_globals_line(None, jsglobals)
            output.append(globals_line)
            in_start_comment = False

        if not is_comment_line(line):
            in_start_comment = False

        output.append(line)

    return "\n".join(output)


def replace_existing_globals(text, jsglobals):
    """
    Replace existing /* globals */ line in the text file
    """
    output = []

    for line in text.split("\n"):
        if is_globals_line(line):
            line = generate_globals_line(line, jsglobals)

        output.append(line)

    return "\n".join(output)


def in_place_replace(fname, text):
    """ Atomic replace of file contents.

    http://stackoverflow.com/a/39110/315168
    """

    path = os.path.dirname(fname)
    tmp = tempfile.NamedTemporaryFile(dir=path, mode="wt", delete=False)
    tmp.write(text)
    tmp.close()
    move(tmp.name, fname)


def process_text(text, jsglobals):
    """
    """
    current_globals_line = None

    jsglobals = jsglobals.split(",")
    jsglobals = [g.strip() for g in jsglobals]

    if len(jsglobals) == 0:
        raise RuntimeError("Where are those globals...")

    for line in text.split("\n"):
        if is_globals_line(line):
            current_globals_line = line

    if current_globals_line:
        text = replace_existing_globals(text, jsglobals)
    else:
        text = add_new_globals_after_comment(text, jsglobals)

    return text


def run(jsglobals, target):
    """
    Process the target file.
    """

    with open(target, "rt") as f:
        text = f.read()
        text = process_text(text, jsglobals)

    in_place_replace(target, text)

    return 0


@plac.annotations(
    jsglobals=("Comma separated list to globals to be added", "positional", None, None, None, "GLOBALSLIST"),
    target=("Javascript file where globals are added. Will be replaced in-place.", "positional", None, None, None, "JSFILE"),
)
def main(jsglobals, target):
    """
    A convenience utility for adding globals declaration to multiple js files

    More info: https://github.com/miohtama/vvv

    Example how to scan the current source tree add add /* globals jQuery, $ */ in every file:

        find . -iname "*.js" | xargs vvv-add-js-globals "$, jQuery"

    Another example - add console global to all JS files under tests:

        find tests -iname "*.js" -print  -exec vvv-add-js-globals "$" {} \;

    Note that the replce is smart and does not destroy existing global declarations.
    The script understand /* globals foo, bar */ style declarations and this declaration only.

    NO WARRANTY. USE AT YOUR OWN RISK.
    """
    sys.exit(run(jsglobals, target))


def entry_point():
    """
    Application starting point which parses command line.

    Can be used from other modules too.
    """


    plac.call(main)

if __name__ == "__main__":
    entry_point()



