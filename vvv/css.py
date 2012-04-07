"""

    CSS validation using W3C validator.

    Requirements: 

    http://www.codestyle.org/css/tools/W3C-CSS-Validator.shtml

    http://jigsaw.w3.org/Distrib/jigsaw_2.2.6.tar.gz

    http://www.nic.funet.fi/pub/mirrors/apache.org//velocity/engine/1.7/velocity-1.7.tar.gz

    http://www.nic.funet.fi/pub/mirrors/apache.org//xerces/j/source/Xerces-J-src.2.11.0.tar.gz



"""

# Python imports
import os
from collections import OrderedDict

# Local imports
from vvv.plugin import Plugin
from vvv.utils import get_string_option

from vvv import sysdeps
from vvv import download

# JAR madness... This is why PyPi rocks
download_and_extract = [
    ("jigsaw", "http://jigsaw.w3.org/Distrib/jigsaw_2.2.6.tar.gz"),
    ("velocity", "http://www.nic.funet.fi/pub/mirrors/apache.org//velocity/engine/1.7/velocity-1.7.tar.gz"),
    ("xerces", "http://www.nic.funet.fi/pub/mirrors/apache.org//xerces/j/source/Xerces-J-src.2.11.0.tar.gz"),
    ("commons-lang", "http://www.nic.funet.fi/pub/mirrors/apache.org//commons/lang/binaries/commons-lang3-3.1-bin.tar.gz"),
    ("commons-collections", "http://archive.apache.org/dist/commons/collections/binaries/commons-collections-3.2.1-bin.tar.gz"),
    ("tagsoup", "http://ccil.org/~cowan/XML/tagsoup/tagsoup-1.2.1.jar"),
    ("css-validator", "http://www.w3.org/QA/Tools/css-validator/css-validator.jar"),
]

download_and_extract = OrderedDict(download_and_extract)

# set CLASSPATH=C:\jigsaw\jigsaw\www\servlet\css-validator\css-validator.jar;c:\jigsaw\classes\velocity-1.5.jar;c:\jigsaw\\classes\xerces.jar
# ;c:\jigsaw\classes\jigsaw.jar;c:\jigsaw\classes\xp.jar;
# c:\jigsaw\classes\sax.jar;c:\jigsaw\classes\servlet.jar;c:\jigsaw\classes\Tidy.jar;c:\jigsaw\classes\tagsoup-1.2.jar;
# C:\Jigsaw\classes\commons-lang-2.4.jar;C:\Jigsaw\classes\commons-collections-3.2.1.jar 

class CSSPlugin(Plugin):
    """
    """

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.css_options = get_string_option(self.options, self.id, "extra", None)

        if not self.hint:
            self.hint = "CSS source code did not pass W3C validator http://jigsaw.w3.org/css-validator/"

    def get_default_matchlist(self):
        """
        These files require hard tabs
        """
        return [
            "*.css",
        ]

    def check_install(self):
        """
        See if the last file is downloaded and extracted
        """

        keys = download_and_extract.keys()
        keys = list(keys)

        path = os.path.join(self.installation_path, keys[-1])
        return not os.path.exists(path)

    def check_requirements(self):
        """
        """
        sysdeps.has_java(needed_for="W3C CSS validator http://jigsaw.w3.org/css-validator/DOWNLOAD.html")

    def install(self):
        """
        Download & install the validator app.
        """

        for fname, url in download_and_extract.items():
            path = os.path.join(self.installation_path, fname)
            download.download_and_extract_java_dep(self.logger, path, url)

    def validate(self, fname):
        """
        Run installed CSS validator against a file.
        """
        classpath = ""

        # Java @__@ .... remembered why I hated it

        jigsaw = os.path.join(self.installation_path, "jigsaw")
        validator = os.path.join(self.installation_path, "css-validator.jar")

        classpath += validator + os.pathsep
        classpath += os.path.join(self.installation_path, "velocity-1.5.jar") + os.pathsep
        classpath += os.path.join(self.installation_path, "xerces.jar") + os.pathsep
        classpath += os.path.join(jigsaw, "jigsaw.jar") + os.pathsep
        classpath += os.path.join(jigsaw, "xp.jar") + os.pathsep                
        classpath += os.path.join(jigsaw, "sax.jar") + os.pathsep       
        classpath += os.path.join(jigsaw, "servlet.jar") + os.pathsep       
        classpath += os.path.join(jigsaw, "Tidy.jar") + os.pathsep      
        classpath += os.path.join(jigsaw, "tagsoup-1.2.jar") + os.pathsep

        return self.run_command_line(["java", "-jar", validator, fname], dict(CLASSPATH=classpath))