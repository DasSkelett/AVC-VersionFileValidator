from unittest import TestCase

from validator.ksp_version import KspVersion


class TestKspVersion(TestCase):

    def test_try_parse_valid_string(self):
        v = KspVersion.try_parse('1.2.3.4')
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertEqual(v.build, 4)

    def test_try_parse_valid_dict(self):
        v = KspVersion.try_parse({
            'MAJOR': '9', 'MINOR': '8',
            'PATCH': '7', 'BUILD': '6'
        })
        self.assertIsNotNone(v)
        self.assertEqual(v.major, 9)
        self.assertEqual(v.minor, 8)
        self.assertEqual(v.patch, 7)
        self.assertEqual(v.build, 6)

    def test_try_parse_invalid(self):
        v = KspVersion.try_parse('xxx.yyy.zzz')
        self.assertIsNone(v)

    def test_comp_different_level(self):
        v1 = KspVersion('1.2.3')
        v2 = KspVersion('1.2')

        self.assertEqual(v1, v2)
        self.assertFalse(v1 < v2)
        self.assertFalse(v1 > v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v2 > v1)

    def test_is_contained_in_true(self):
        v_latest_ksp = KspVersion('1.8.1')
        v_ksp = KspVersion('1.8')
        v_ksp_min = KspVersion('1.7')
        v_ksp_max = KspVersion('1.8.9')

        self.assertTrue(v_latest_ksp.is_contained_in(v_ksp, None, None))
        self.assertTrue(v_latest_ksp.is_contained_in(None, v_ksp_min, None))
        self.assertTrue(v_latest_ksp.is_contained_in(None, None, v_ksp_max))
        self.assertTrue(v_latest_ksp.is_contained_in(v_ksp, v_ksp_min, v_ksp_max))

    def test_is_contained_in_newer_ksp(self):
        v_latest_ksp = KspVersion('1.9.1')
        v_ksp = KspVersion('1.8')
        v_ksp_min = KspVersion('1.7')
        v_ksp_max = KspVersion('1.8.9')

        self.assertFalse(v_latest_ksp.is_contained_in(v_ksp, None, None))
        self.assertTrue(v_latest_ksp.is_contained_in(None, v_ksp_min, None))
        self.assertFalse(v_latest_ksp.is_contained_in(None, None, v_ksp_max))
        self.assertFalse(v_latest_ksp.is_contained_in(v_ksp, v_ksp_min, v_ksp_max))
