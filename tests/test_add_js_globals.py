"""

    test addjsglobals.py for various JS file styles

"""

import unittest

from vvv.scripts import addjsglobals

test_cases = [
# Empty line at start
(
"""
function foobar() {
}
""",
# -->
"""/*global jQuery, $ */

function foobar() {
}
"""
),

# No Empty line at start
(
"""function foobar() {
}
""",
# -->
"""/*global jQuery, $ */
function foobar() {
}
"""
),

# Comment at start 
(
"""/**
 * My comment
 *
 */
function foobar() {
}
""",
# -->
"""/**
 * My comment
 *
 */
/*global jQuery, $ */
function foobar() {
}
"""
),

# Comment after empty line
(
"""
/**
 * My comment
 *
 */
function foobar() {
}
""",
# -->
"""/*global jQuery, $ */

/**
 * My comment
 *
 */
function foobar() {
}
"""
),

# Replace existing after comment
(
"""/**
 * My comment
 *
 */
/* global window */
function foobar() {
}
""",
# -->
"""/**
 * My comment
 *
 */
/*global window, jQuery, $ */
function foobar() {
}
"""
),

# Replace existing, no start comment
(
"""
/* global window */
function foobar() {
}
""",
# -->
"""
/*global window, jQuery, $ */
function foobar() {
}
"""
),

]

class TestAddJsGlobals(unittest.TestCase):
    """
    Test our little helper script
    """



    @staticmethod
    def run_script(text):
        """
        """
        text = addjsglobals.process_text(text, "jQuery, $")
        return text


    def test_process_text(self):
        for intext, outtext in test_cases:
            result = self.run_script(intext)
            self.assertEqual(result, outtext)

