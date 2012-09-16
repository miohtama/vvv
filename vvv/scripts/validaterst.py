"""

    Simple script to validate rst files, patched to ignore Unknown directive errors

    Based on rst2html http://docutils.svn.sourceforge.net/viewvc/docutils/trunk/docutils/tools/rst2html.py?revision=4564&view=markup



"""

import sys
import os

# http://const-cast.blogspot.com/2009/04/mercurial-on-mac-os-x-valueerror.html

try:
    from docutils import utils
except ValueError as v:
    if str(v) == "unknown locale: UTF-8":
        print("Your have misconfigured shell, probably caused by http://const-cast.blogspot.com/2009/04/mercurial-on-mac-os-x-valueerror.html")
        print("Do:")
        print("export LC_ALL=en_US.UTF-8")
        print("export LANG=en_US.UTF-8")
    raise

from docutils.core import publish_parts

reports = []

#
# Monkey patch crap out of docutils
#

orignal_system_message = utils.Reporter.system_message


# 'No directive entry for "automodule" in module "docutils.parsers.rst.languages.en".\nTrying "automodule" as canonical directive name.'
# <string>:23: (ERROR/3) Unknown interpreted text role "ref"
# 'No role entry for "doc" in module "docutils.parsers.rst.languages.en".\nTrying "doc" as canonical role name.'
def filter_message(message):
    """
    Return True if message is valid output
    """
    # <string>:7: (ERROR/3) Unknown directive type "automodule".
    if "No directive entry for" in message or "Unknown directive type" in message \
        or "Unknown interpreted text role" in message \
            or "No role entry for" in message:

        return False
    return True


def system_message(self, level, message, *children, **kwargs):
    """
    Patched system message to collect filtered output to a list

    http://docutils.svn.sourceforge.net/viewvc/docutils/trunk/docutils/docutils/utils/__init__.py?revision=7338&view=markup
    """

    if filter_message(message):

        result = orignal_system_message(self, level, message, *children, **kwargs)

        if level >= self.WARNING_LEVEL:

            # Collect to internal message log
            reports.append(message)

    else:
        # We don't want to see the filtered messages
        result = orignal_system_message(self, self.DEBUG_LEVEL, message, *children, **kwargs)

    # All reST failures preventing doc publishing go to reports
    # and thus will result to failed checkdocs run
    return result

# Monkeypatch docutils for simple error/warning output support
utils.Reporter.system_message = system_message


def rst2html(value):
    """ Run rst2html translation """
    parts = publish_parts(source=value)
    return parts['whole']


def run():
    """
    """

    if len(sys.argv) < 2:
        print("Usage: vvv-validate-rst [filename.rst]")
        sys.exit(2)

    fname = sys.argv[1]
    f = open(fname, "rt")
    text = f.read()
    f.close()

    # Monkeypatch docutils for simple error/warning output support
    utils.Reporter.system_message = system_message

    absolute_dir = os.path.dirname(os.path.abspath(fname))
    prev_work_dir = os.getcwd()
    os.chdir(absolute_dir)
    rst2html(text)
    os.chdir(prev_work_dir)

    if len(reports) > 0:
        print(reports)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    run()
