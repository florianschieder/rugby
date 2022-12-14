from unittest import TestCase

from rugby import sum as rugby_sum


class SumTests(TestCase):
    def test_sum(self):
        self.assertEqual(55, rugby_sum(0, 10))