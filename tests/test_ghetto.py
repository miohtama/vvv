"""

    Test Ghetto CI.

"""

"""

    test addjsglobals.py for various JS file styles

"""

import unittest

from vvv.scripts import addjsglobals


class TestGhetto(unittest.TestCase):
    """
    Test our little helper script
    """

    def test_import(self):
        """
        See that script imports both Python 2.7 and Python 3.x
        """
        import ghettoci