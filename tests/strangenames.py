import os
from pathlib import Path
from unittest import TestCase

import validator.validator as validator


class TestStrangeNames(TestCase):
    old_cwd = os.getcwd()

    @classmethod
    def setUpClass(cls):
        os.chdir('./tests/workspaces/strange-names')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_cwd)

    def test_findsAll(self):
        (status, successful, failed, ignored) = validator.validate_cwd('')
        self.assertEqual(status, 1)
        self.assertSetEqual(successful, {Path('CAPS.VERSION')})
        self.assertSetEqual(failed, {Path('camelCaseVersionMissing.Version')})
        # Make sure 'not-detected.version.json' has not been detected.
        self.assertSetEqual(ignored, set())
