import unittest
import elftasks
import numpy
from io import StringIO
from collections import deque


if __name__ == '__main__':
    unittest.main()



class TestDay1(unittest.TestCase):
    def test_task1(self):
        self.assertEqual(False, elftasks.day1())