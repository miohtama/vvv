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

# unittest method names do not satisfy PEP-8
# :C0103: *Invalid name "%s" (should match %s)*
# :W0201: *Attribute %r defined outside __init__*
# :W0603: *Using the global statement*
# pylint: disable = C0103, W0201, W0603

import unittest
import os
import sys
import shutil

from vvv.main import VVV

VERBOSE = os.environ.get("VVV_TEST_OUTPUT", None) == "verbose"

SKIP_REINSTALL = os.environ.get("VVV_TEST_SKIP_REINSTALL", None) == "true"

TEST_CASE_FILTER = os.environ.get("VVV_TEST_FILTER", None)

#: Are we the first test case to be executed
first_run = True

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

    def __init__(self, *args, **kwargs):
        """
        """
        unittest.TestCase.__init__(self, *args, **kwargs)

    def set_path(self, path, success, options):
        """
        Set path to a "project source folder" which we execute.

        :param path: Full path to the folder

        :param success: Should test data validate or not
        """
        # XXX: Set set static class members,
        # no need to call this method
        self.path = path
        self.success = success
        self.options = options

    @staticmethod
    def get_install_path():
        """
        """
        get_own_path()
        install_path = os.path.join(get_own_path(), "test-installation-environment")
        return install_path

    def nuke_installations_by_test_case(self):
        """
        Delete and reconfigure .vvv validator installations between tests if the test says so. 

        XXX: Not supported currently
        """ 

        # test-options.yaml reinstall option gives installation names to nuke
        # E.g. reinstall: pylint 
        reinstall = self.options.get("reinstall", "")
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

        global first_run 

        # Set output level
        verbose = VERBOSE
        quiet = not VERBOSE

        # Set test installation folder
        install_path = self.get_install_path()

        # Ugh.... does not make me proud
        reinstall = first_run 

        if SKIP_REINSTALL:
            reinstall = False

        first_run = False

        # Run 
        vvv = VVV(target=self.path, 
                  quiet=quiet, 
                  verbose=verbose, 
                  installation=install_path, 
                  reinstall=reinstall,
                  options=self.options)

        vvv.set_project_path(self.path)
        
        result = vvv.run()

        if vvv.output:
            self.assertFalse("Line contains hard tabs" in vvv.output, "Please fix tab errors in the test cases first %s" % self.path)

        success = (result == 0)
        if success:
            self.assertTrue(self.success, "Test folder %s should have failed, but succeeded:\nOutput:\n%s" % (self.path, vvv.output))

        if not success:
            self.assertFalse(self.success, "Test folder %s should have passed, but failed.\nOutput:\n%s" % (self.path, vvv.output))

def scan_test_cases():
    """
    Find validator test folder.

    Add folders ending with -pass or -fail to the test queue.

    :return: List of tuples (fullname, name, success, Config file path)
    """

    out = []

    path = os.path.join(get_own_path(), "validators")

    # W:100,10:Unused variable'
    # pylint: disable = W0612    

    for root, dirs, files in os.walk(path):
        for d in dirs:

            fullname = os.path.join(root, d)
            relative_root = fullname[len(path)+1:]
            name = relative_root.replace("-", "_").replace(os.sep, "_")

            if TEST_CASE_FILTER:
                if not TEST_CASE_FILTER in name:
                    continue
    
            # Read test driver options
            options = os.path.join(fullname, "validation-options.yaml")
            if not os.path.exists(options):
                # No optinos for this test case
                options = None

            if d.endswith("-pass"):
                out.append((fullname, name, True, options))
            if d.endswith("-fail"):
                out.append((fullname, name, False, options))

            

    return out

def create_test_case_class(name, path, success, options):
    """
    Spoofs out Python TestCase class which matches folder name.
    """

    klass = type(
           name,
           (ValidatorTestCase,),
           dict(path=path, success=success, options=options)
           )
    return klass


# :W0613: *Unused argument %r*
# pylint: disable = W0613   

def load_tests(loader, standard_tests, wtf_is_this_third_argument):
    """
    http://docs.python.org/dev/library/unittest.html

    python -m unittest discover hook
    """
    validation_suite = unittest.TestSuite()

    cases = scan_test_cases()
    for c in cases:
        klass = create_test_case_class(c[1], c[0], c[2], c[3])
        tests = loader.loadTestsFromTestCase(klass)
        validation_suite.addTest(tests)

    return validation_suite

if __name__ == '__main__':
    
    if VERBOSE:
        verbosity = 3
    else: 
        verbosity = 0
    
    suite = load_tests(unittest.TestLoader(), None, None)
    unittest.TextTestRunner(verbosity=verbosity).run(suite) 