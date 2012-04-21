"""

CSS (W3C validator)
====================

Validator name: ``css``

Validate CSS files against W3C CSS validator.

Prerequisites
----------------
      
Your system must have Java installed and support and ``java`` command.      

Please see :doc:`prerequisites </prerequisites>`.

Installation
----------------

CSS validator is Java executable and bunch of JAR files
which are downloaded and installed automatically.

Supported files
----------------

* \*.css

Options
-----------

command-line
+++++++++++++

Command line arguments passed to W3C validator.

Default::

    --profile=css3

Troubleshooting
----------------------

If you get error::

    Exception in thread "main" java.lang.NoClassDefFoundError: org/w3c/tools/resources/ProtocolException
    Caused by: java.lang.ClassNotFoundException: org.w3c.tools.resources.ProtocolException
        at java.net.URLClassLoader$1.run(URLClassLoader.java:202)
        at java.security.AccessController.doPrivileged(Native Method)
        at java.net.URLClassLoader.findClass(URLClassLoader.java:190)
        at java.lang.ClassLoader.loadClass(ClassLoader.java:306)
        at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:301)
        at java.lang.ClassLoader.loadClass(ClassLoader.java:247)

It is probably caused by a broken automatic W3C validator installation and you can fix it with::

    rm -rf ~/.vvv/css 

More info
------------

* http://jigsaw.w3.org/css-validator/

* http://dev.w3.org/cvsweb/2002/css-validator/org/w3c/css/css/CssValidator.java?rev=1.15

"""

# Python imports
import os
from collections import OrderedDict

# Local imports
from vvv.plugin import Plugin
#from vvv.utils import get_string_option

from vvv import sysdeps
from vvv import download

#: Command-line options given to the validator always
DEFAULT_COMMAND_LINE = "--profile=css3"

# JAR madness... This is why PyPi rocks
DOWNLOAD_AND_EXTRACT = [
    ("jigsaw.tar.gz", "http://jigsaw.w3.org/Distrib/jigsaw_2.2.6.tar.gz"),
    ("velocity.tar.gz", "http://www.nic.funet.fi/pub/mirrors/apache.org//velocity/engine/1.7/velocity-1.7.tar.gz"),
    ("xerces.tar.gz", "http://www.nic.funet.fi/pub/mirrors/apache.org//xerces/j/source/Xerces-J-src.2.11.0.tar.gz"),
    ("commons-lang.tar.gz", "http://www.nic.funet.fi/pub/mirrors/apache.org//commons/lang/binaries/commons-lang3-3.1-bin.tar.gz"),
    ("commons-collections.tar.gz", "http://archive.apache.org/dist/commons/collections/binaries/commons-collections-3.2.1-bin.tar.gz"),
    ("tagsoup.jar", "http://ccil.org/~cowan/XML/tagsoup/tagsoup-1.2.1.jar"),
    ("css-validator.jar", "http://www.w3.org/QA/Tools/css-validator/css-validator.jar"),
]

DOWNLOAD_AND_EXTRACT = OrderedDict(DOWNLOAD_AND_EXTRACT)

# set CLASSPATH=C:\jigsaw\jigsaw\www\servlet\css-validator\css-validator.jar;c:\jigsaw\classes\velocity-1.5.jar;c:\jigsaw\\classes\xerces.jar
# ;c:\jigsaw\classes\jigsaw.jar;c:\jigsaw\classes\xp.jar;
# c:\jigsaw\classes\sax.jar;c:\jigsaw\classes\servlet.jar;c:\jigsaw\classes\Tidy.jar;c:\jigsaw\classes\tagsoup-1.2.jar;
# C:\Jigsaw\classes\commons-lang-2.4.jar;C:\Jigsaw\classes\commons-collections-3.2.1.jar 

#: If these are found in the output assume CSS validation failed
VALIDATOR_ERRORS = ["Sorry!", 'Exception in thread "main"']

class CSSPlugin(Plugin):
    """
    W3C CSS validator driver.
    """

    def __init__(self):

        Plugin.__init__(self)

        #: Commandl line options passed to the validator from the config file
        self.extra_options = None        

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = self.options.get_string_option(self.id, "command-line", DEFAULT_COMMAND_LINE)

        if not self.hint:
            self.hint = "CSS source code did not pass W3C validator http://jigsaw.w3.org/css-validator/"

    def get_default_matchlist(self):
        """
        These files go into the validator.
        """
        return [
            "*.css",
        ]

    def check_is_installed(self):
        """
        See if the last file is downloaded and extracted
        """

        keys = DOWNLOAD_AND_EXTRACT.keys()
        keys = list(keys)

        path = os.path.join(self.installation_path, keys[-1])
        return os.path.exists(path)

    def check_requirements(self):
        """
        """
        sysdeps.has_java(needed_for="W3C CSS validator http://jigsaw.w3.org/css-validator/DOWNLOAD.html")

    def install(self):
        """
        Download & install the validator app.
        """

        for fname, url in DOWNLOAD_AND_EXTRACT.items():
            path = os.path.join(self.installation_path, fname)
            download.download_and_extract_java_dep(self.logger, path, url)

    def validate(self, fname):
        """
        Run installed CSS validator against a file.
        """
        classpath = ""

        fullpath = os.path.abspath(fname)

        # Java @__@ .... remembered why I hated it

        jigsaw = os.path.join(self.installation_path, "jigsaw", "Jigsaw", "classes")
        validator = os.path.join(self.installation_path, "css-validator.jar")

        classpath += validator + os.pathsep
        # XXX: Fix for Windows
        classpath += os.path.join(self.installation_path, "velocity/velocity-1.7/velocity-1.7-dep.jar") + os.pathsep
        classpath += os.path.join(self.installation_path, "velocity/velocity-1.7/velocity-1.7.jar") + os.pathsep
        classpath += os.path.join(jigsaw, "xerces.jar") + os.pathsep
        classpath += os.path.join(jigsaw, "jigsaw.jar") + os.pathsep
        classpath += os.path.join(jigsaw, "xp.jar") + os.pathsep                
        classpath += os.path.join(jigsaw, "sax.jar") + os.pathsep       
        classpath += os.path.join(jigsaw, "servlet.jar") + os.pathsep       
        classpath += os.path.join(jigsaw, "Tidy.jar") + os.pathsep      
        classpath += os.path.join(jigsaw, "tagsoup-1.2.jar")

        # XXX: We should not split here, but pass in command line optons
        # as shell string 
        options = self.extra_options.split()

        cmdline = ["java", "org.w3c.css.css.CssValidator"]
        cmdline += options
        cmdline += ["file://" + fullpath]

        # W3C prints out all valid CSS and we are not really interested in that... 
        # It prints valid CSS as last and we simply crop this tail out
        snip = "Valid CSS information"

        # ...does not even have return code...
        return self.run_command_line(cmdline, bad_string=VALIDATOR_ERRORS, snip_string=snip, env=dict(CLASSPATH=classpath))
