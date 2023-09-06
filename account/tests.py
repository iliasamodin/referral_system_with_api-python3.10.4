from django.test import TestCase
from functions import convert_to_another_system
import unittest


class TestConvertToAnotherSystem(unittest.TestCase):
    def test_result_1(self):
        self.assertEqual(convert_to_another_system(13, 2), bin(13)[2:])

    def test_result_2(self):
        self.assertEqual(convert_to_another_system(89, 8), oct(89)[2:])

    def test_result_3(self):
        self.assertEqual(
            convert_to_another_system(233, 16), 
            hex(233)[2:].upper()
        )

    def test_result_4(self):
        self.assertEqual(convert_to_another_system(1597, 20), "3JH")

    def test_result_5(self):
        self.assertEqual(convert_to_another_system(28657, 36), "M41")


if __name__ == "__main__":
    unittest.main()