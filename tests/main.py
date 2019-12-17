import os
from unittest import TestCase

import validator.main as validator


class TestMain(TestCase):
    os.chdir('./tests/workspaces/default')

    def test_validWorkspace_excludes_recursive(self):
        self.assertEqual(0, validator.validate('recursiveness/failing-validation.version'))

    def test_invalidWorkspace_recursive(self):
        self.assertEqual(1, validator.validate(''))
