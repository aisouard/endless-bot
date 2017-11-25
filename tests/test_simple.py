from unittest import TestCase


class TestSimple(TestCase):
    def test_is_string(self):
        s = 'hello'
        self.assertTrue(isinstance(s, str))
