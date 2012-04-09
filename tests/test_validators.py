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

"""

import unittest
import os
import sys

from vvv.main import VVV

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

        
    def runTest(self):
        """
        Execute vvv in a folder and check the output.
        """

        # Set output level
        verbose = VERBOSE
        quiet = not VERBOSE

        # Set test installation folder
        install_path = get_own_path()
        install_path = os.path.join(install_path, "test-installation-environment")

        # Ugh.... does not make me proud
        reinstall = not ValidatorTestCase.first_run and REINSTALL


        ValidatorTestCase.first_run = False

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

    :return: List of tuples (fullname, name, success)
    """

    out = []

    path = os.path.join(get_own_path(), "validators")

    for root, dirs, files in os.walk(path):
        for d in dirs:

            fullname = os.path.join(root, d)

            if d.endswith("-pass"):
                out.append((fullname, d, True))
            if d.endswith("-fail"):
                out.append((fullname, d, False))

    return out

def create_test_case_class(name, path, success):
    """
    Spoofs out Python TestCase class which matches folder name.
    """

    klass = type(
           'name',
           (ValidatorTestCase,),
           dict(path=path, success=success)
           )
    return klass

def load_tests(loader, standard_tests, wtf_is_this_third_argument):
    """
    http://docs.python.org/dev/library/unittest.html
    """
    suite = unittest.TestSuite()

    cases = scan_test_cases()
    for c in cases:
        klass = create_test_case_class(c[1], c[0], c[2])
        tests = loader.loadTestsFromTestCase(klass)
        suite.addTest(tests)

    return suite

if __name__ == '__main__':
    unittest.main()    