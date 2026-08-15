import re
import unittest

import action0.open_meteo


class PackageTestCase(unittest.TestCase):
    """
    tests for the package root
    """

    def test_version(self) -> None:
        """
        Test that the version is a PEP-440-ish dotted number.
        """
        self.assertRegex(action0.open_meteo.__version__, re.compile(r"^\d+\.\d+\.\d+"))
