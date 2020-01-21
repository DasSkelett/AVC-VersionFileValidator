import os
from pathlib import Path
from unittest import TestCase

import validator.validator as validator


class TestSingleFiles(TestCase):
    old_cwd = os.getcwd()

    @classmethod
    def setUpClass(cls):
        os.chdir('./tests/workspaces/single-files')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_cwd)

    def test_invalidRemote(self):
        (status, successful, failed, ignored) = validator.validate('')
        self.assertIn(Path('invalid-remote.version'), failed)

    def test_validRemote(self):
        (status, successful, failed, ignored) = validator.validate('')
        self.assertIn(Path('valid-remote.version'), successful)
