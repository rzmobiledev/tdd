"""
Sample test
"""
from django.test import SimpleTestCase
from admin import calc


class CalcTest(SimpleTestCase):

    """Test calc module"""

    def test_add_number(self):

        """Test adding numbers together"""
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_substract_number(self):
        """Test substracting numbers"""
        res = calc.substract(10, 15)
        self.assertEqual(res, 5)
