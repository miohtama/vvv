"""

    Simple script to validate rst files, ignoring Unknown directive errors

    Based on rst2html http://docutils.svn.sourceforge.net/viewvc/docutils/trunk/docutils/tools/rst2html.py?revision=4564&view=markup

"""

import sys

#
# Monkey patch crap out of docutils
#

try:
    from docutils import utils
except ValueError as v:
    if str(v) == "unknown locale: UTF-8": 
        print("Your have misconfigured shell, probably caused by http://const-cast.blogspot.com/2009/04/mercurial-on-mac-os-x-valueerror.html")
    raise

from docutils.core import publish_parts

reports = []

orignal_system_message = utils.Reporter.system_message

# 'No directive entry for "automodule" in module "docutils.parsers.rst.languages.en".\nTrying "automodule" as canonical directive name.'
def filter_message(message):
    """ """
    # <string>:7: (ERROR/3) Unknown directive type "automodule".
    if "'No directive entry for" in message:
        return False
    return True 

def system_message(self, level, message, *children, **kwargs):
    """
    Patched system message to collect filtered output to a list

    http://docutils.svn.sourceforge.net/viewvc/docutils/trunk/docutils/docutils/utils/__init__.py?revision=7338&view=markup
    """

    if filter_message(message):
        # We don't want to see the filtered messages
        result = orignal_system_message(self, self.DEBUG_LEVEL, message, *children, **kwargs)
    else:

        result = orignal_system_message(self, level, message, *children, **kwargs)

        # Collect to internal message log
        reports.append(message)

    # All reST failures preventing doc publishing go to reports 
    # and thus will result to failed checkdocs run
    return result

# Monkeypatch docutils for simple error/warning output support
utils.Reporter.system_message = system_message    

def rst2html(value):
    """ Run rst2html translation """
    docutils_settings = {}
    #parts = publish_parts(source=value, writer_name="html4css1")
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

    html = rst2html(text)

    if len(reports) > 0:
        sys.exit(1)
       
    sys.exit(0)

if __name__ == "__main__":
    run()    

      