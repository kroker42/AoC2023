import unittest
import elftasks

if __name__ == '__main__':
    unittest.main()


class TestDay1(unittest.TestCase):
    data = "\
twoone \
two1nine \
eightwothree \
abcone2threexyz \
xtwone3four \
4nineeightseven2 \
zoneight234 \
7pqrstsixteen"
    def test_task1(self):
        nums = elftasks.match_digits(self.data.split())
        self.assertEqual(["21", "219", "823", "123", "2134", "49872", "18234", "76"], ["".join(x) for x in nums])



