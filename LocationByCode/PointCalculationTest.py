import unittest

class PCtest(unittest.TestCase):
    
    def test_String(self):
        self.assertEqual("123","123")

if __name__ == "__main__":
        unittest.main()  # py .\PointCalculationTest.py -v         -->      use -v to get more information

