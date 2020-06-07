import os
from unittest import TestCase

from validator.utils import get_env_array


class TestUtils(TestCase):
    def test_getEnvArray(self):
        os.environ['INPUT_ONLY'] = '["fileA.version", "fileB.txt"]'
        self.assertEquals(get_env_array('INPUT_ONLY'), ['fileA.version', 'fileB.txt'])
