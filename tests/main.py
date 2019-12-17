import os
from pathlib import Path
from unittest import TestCase

import validator.main as validator


class TestDefault(TestCase):
    os.chdir('./tests/workspaces/default')

    def test_validWorkspace_excludes_recursive(self):
        (status, successful, failed, ignored) = validator.validate('recursiveness/failing-validation.version')
        self.assertEqual(status, 0)

    def test_invalidWorkspace_recursive(self):
        (status, successful, failed, ignored) = validator.validate('')
        self.assertEqual(status, 1)

    def test_exclusionWildcard(self):
        (status, successful, failed, ignored) = validator.validate('recursiveness/*')
        print(ignored)
        self.assertEqual(status, 0)
        # assertCountEqual() has a misleading name. It _does_ also check whether the elements in the lists are the same,
        # ignoring their order. Not only the item count.
        self.assertCountEqual(successful, [Path('default.version')])
        self.assertCountEqual(ignored,
                              [Path('recursiveness/failing-validation.version'),
                               Path('recursiveness/recursive.version')])
        self.assertEqual(failed, [])
