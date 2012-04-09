"""

    Test vvv validators against known good / bad test cases.

    This will stress

    * Each validator downloads and installs correctly

    * Each validator can report success / failure

    .. note ::
        
        Test cases here do no really satisfy the criteria of being atomic,
        as the installation folder is shared between test cases.

    .. note ::

        Running the tests will always reload all crap from the internets
        and perform local installs.

    The script will scan ``validator`` subfolders. If folder name 
    ends with -pass or -fail it is considered a test case.
    VVV is run against this folder. The folder may give its
    own ``validation-options.yaml`` file.

"""

import unittest
import os
import sys
import shutil

from vvv.main import VVV
from vvv import utils

VERBOSE = os.environ.get("VVV_TEST_OUTPUT", "verbose")

REINSTALL = os.environ.get("VVV_TEST_REINSTALL", None) != "false"

def get_own_path():
    """
    Get path of this Python module.
    """
    module = sys.modules[__name__]
    path = os.path.dirname(module.__file__)
    return path

class ValidatorTestCase(unittest.TestCase):
    """
    Wraps executing vvv process to Python unittest framework.
    """

    first_run = False

    def set_path(self, path, success):
        """
        Set path to a "project source folder" which we execute.

        :param path: Full path to the folder

        :param success: Should test data validate or not
        """
        self.path = path
        self.succes = success

    def get_install_path(self):
        """
        """
        get_own_path()
        install_path = os.path.join(get_own_path(), "test-installation-environment")
        return install_path

    def nuke_installations(self):
        """
        Delete and reconfigure .vvv validator installations between tests if the test says so. 
        """ 

        # test-options.yaml reinstall option gives installation names to nuke
        # E.g. reinstall: pylint 
        reinstall = self.options.get("reinstall")
        if type(reinstall) != list:
            reinstall = reinstall.split()

        for installation in reinstall:
            path = os.path.join(self.get_install_path(), installation)
            if os.path.exists(path):
                shutil.rmtree(path)
        
    def runTest(self):
        """
        Execute vvv in a folder and check the output.
        """

        # Set output level
        verbose = VERBOSE
        quiet = not VERBOSE

        # Set test installation folder
        install_path = self.get_install_path()

        # Ugh.... does not make me proud
        reinstall = not ValidatorTestCase.first_run and REINSTALL

        ValidatorTestCase.first_run = False

        self.nuke_installations()

        # Run 
        vvv = VVV(project=self.path, 
                  quiet=quiet, 
                  verbose=verbose, 
                  installation=install_path, 
                  reinstall=reinstall)
        
        result = vvv.run()

        success = (result == 0)
        if success:
            self.assertTrue(self.success, "Test folder %s should have failed, but succeeded" % self.path)

        if not success:
            self.assertFalse(self.success, "Test folder %s should have passed, but failed. Run env option VVV_TEST_OUTPUT=verbose for more output" % self.path)

def scan_test_cases():
    """
    Find validator test folder.

    Add folders ending with -pass or -fail to the test queue.

    :return: List of tuples (fullname, name, success, options)
    """

    out = []

    path = os.path.join(get_own_path(), "validators")

    for root, dirs, files in os.walk(path):
        for d in dirs:

            fullname = os.path.join(root, d)

            # Read test driver options
            options = utils.load_yaml_file(os.path.join(fullname, "test-options.yaml"))


            if d.endswith("-pass"):
                out.append((fullname, d, True, options))
            if d.endswith("-fail"):
                out.append((fullname, d, False, options))

            

    return out

def create_test_case_class(name, path, success, options):
    """
    Spoofs out Python TestCase class which matches folder name.
    """

    klass = type(
           'name',
           (ValidatorTestCase,),
           dict(path=path, success=success, options=options)
           )
    return klass

def load_tests(loader, standard_tests, wtf_is_this_third_argument):
    """
    http://docs.python.org/dev/library/unittest.html
    """
    suite = unittest.TestSuite()

    cases = scan_test_cases()
    for c in cases:
        klass = create_test_case_class(c[1], c[0], c[2], c[3])
        tests = loader.loadTestsFromTestCase(klass)
        suite.addTest(tests)

    return suite

if __name__ == '__main__':
    if VERBOSE:
        verbosity = 3
    else: 
        verbosity = 0
    unittest.main(verbosity=verbosity)    