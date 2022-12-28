from unittest import TestCase

from rugby import (
    sum as rugby_sum,
    greet as rugby_greet,
)


class SumTests(TestCase):
    def test_sum(self):
        self.assertEqual(55, rugby_sum(0, 10))


class GreetTests(TestCase):
    def test_greet(self):
        self.assertEqual("Hello dev!", rugby_greet("dev"))
