import os
from pathlib import Path
from unittest import TestCase

import validator.validator as validator
from .test_utils import schema, build_map


class TestDefault(TestCase):
    old_cwd = os.getcwd()

    @classmethod
    def setUpClass(cls):
        os.chdir('./tests/workspaces/default')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_cwd)

    def test_doubleQuotation(self):
        (status, successful, failed, ignored) = validator.validate_cwd(
            '"failing/failing-validation.version"', schema, build_map)
        self.assertEqual(status, 0)

    def test_invalidWorkspace_recursive(self):
        (status, successful, failed, ignored) = validator.validate_cwd('', schema, build_map)
        self.assertEqual(status, 1)

    def test_exclusionWildcard(self):
        (status, successful, failed, ignored) = validator.validate_cwd('failing/*.version', schema, build_map)
        self.assertEqual(status, 0)
        self.assertSetEqual(successful, {Path('default.version'), Path('recursiveness/recursive.version'),
                                         Path('recursiveness/recursiveness2/recursive2.version')})
        self.assertSetEqual(ignored, {Path('failing/failing-validation.version')})
        self.assertEqual(failed, set())

    def test_excludeAll(self):
        (status, successful, failed, ignored) = validator.validate_cwd('["./**/*"]', schema, build_map)
        self.assertEqual(status, 0)
        self.assertSetEqual(successful, set())
        self.assertSetEqual(ignored, {Path('default.version'),
                                      Path('failing/failing-validation.version'),
                                      Path('recursiveness/recursive.version'),
                                      Path('recursiveness/recursiveness2/recursive2.version')})
        self.assertEqual(failed, set())

    def test_recursiveExclusion(self):
        (status, successful, failed, ignored) = validator.validate_cwd('["./recursiveness/**/*"]',
                                                                       schema, build_map)
        self.assertEqual(status, 1)
        self.assertSetEqual(successful, {Path('default.version')})
        self.assertSetEqual(ignored, {Path('recursiveness/recursive.version'),
                                      Path('recursiveness/recursiveness2/recursive2.version')})
        self.assertEqual(failed, {Path('failing/failing-validation.version')})

    def test_multipleExclusions(self):
        (status, successful, failed, ignored) = validator.validate_cwd('["./*.version", "./failing/*"]',
                                                                       schema, build_map)
        self.assertEqual(status, 0)
        self.assertSetEqual(successful, {Path('recursiveness/recursive.version'),
                                         Path('recursiveness/recursiveness2/recursive2.version')})
        self.assertSetEqual(ignored, {Path('default.version'), Path('failing/failing-validation.version')})
        self.assertEqual(failed, set())
