from unittest import TestCase

from validator.versionfile import get_raw_uri


class TestVersionFile(TestCase):

    def test_getRawUri_blob(self):
        before = 'https://github.com/DasSkelett/AVC-VersionFileValidator/blob/master/README.md'
        expect_after = 'https://github.com/DasSkelett/AVC-VersionFileValidator/raw/master/README.md'

        got_after = get_raw_uri(before)

        self.assertEqual(expect_after, got_after)

    def test_getRawUri_tree(self):
        before = 'https://github.com/DasSkelett/AVC-VersionFileValidator/tree/master/README.md'
        expect_after = 'https://github.com/DasSkelett/AVC-VersionFileValidator/raw/master/README.md'

        got_after = get_raw_uri(before)

        self.assertEqual(expect_after, got_after)

    def test_getRawUri_doubleBlob(self):
        before = 'https://github.com/DasSkelett/AVC-VersionFileValidator/blob/master/blob/README.md'
        expect_after = 'https://github.com/DasSkelett/AVC-VersionFileValidator/raw/master/blob/README.md'

        got_after = get_raw_uri(before)

        self.assertEqual(expect_after, got_after)

    def test_getRawUri_noGH(self):
        before = 'https://no-github.com/DasSkelett/AVC-VersionFileValidator/tree/master/README.md'

        got_after = get_raw_uri(before)

        self.assertEqual(before, got_after)
