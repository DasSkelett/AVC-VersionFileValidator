import json
import os
from pathlib import Path
from unittest import TestCase

import validator.validator as validator
from validator.versionfile import VersionFile
from .test_utils import schema, build_map


class TestSingleFiles(TestCase):
    old_cwd = os.getcwd()

    @classmethod
    def setUpClass(cls):
        os.chdir('./tests/workspaces/single-files')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_cwd)

    def test_invalidRemote(self):
        f = Path('./invalid-remote.version')
        with f.open('r') as vf:
            version_file = VersionFile(vf.read())
            with self.assertRaises(json.decoder.JSONDecodeError):
                remote = version_file.get_remote()

    def test_validRemote(self):
        (status, successful, failed, ignored) = validator.validate_cwd('', schema, build_map)
        self.assertIn(Path('valid-remote.version'), successful)
