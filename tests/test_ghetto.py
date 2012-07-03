"""

    Test Ghetto CI.

"""


import unittest

# R0201: 21,4:TestGhetto.test_import: Method could be a function
# pylint: disable=R0201


class TestGhetto(unittest.TestCase):
    """
    Test our little helper script
    """

    def test_import(self):
        """
        See that script imports both Python 2.7 and Python 3.x
        """
        import ghettoci
        ghettoci.POkE = True
