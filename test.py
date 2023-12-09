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

#####################################

class TestDay3(unittest.TestCase):
    data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    def test_task2(self):
        grid = self.data.split("\n")
        gears = elftasks.find_gears(grid)
        self.assertEqual(467835, sum(gears))



###############


class TestDay5(unittest.TestCase):
    data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

"""
    def test_seed_parsing(self):
        seeds = elftasks.parse_seeds("seeds: 79 14 55 13")
        self.assertEqual([79, 14, 55, 13], seeds)

        seed_ranges = elftasks.parse_seed_ranges(seeds)
        self.assertEqual([range(79, 93), range(55, 68)], seed_ranges)

    def test_source_dest_map(self):
        data = ["50 98 2", "52 50 48", '']
        destinations = {
            range(98, 100): 50,
            range(50, 98): 52
        }
        self.assertEqual((2, destinations), elftasks.parse_dest_map(data, 0))

        sources = [79, 14, 55, 13]
        self.assertEqual([81, 14, 57, 13], elftasks.get_next_destinations(sources, destinations))


###############


class TestDay9(unittest.TestCase):
    data = """0 3 6 9 12 15
    1 3 6 10 15 21
    10 13 16 21 30 45"""
    data = [[int(x) for x in line.strip().split(" ")] for line in data.split("\n")]

    def test_calc_diffs(self):
        self.assertEqual([[3 * i for i in range(6)], [3] * 5, [0] * 4], elftasks.calc_diff_tree(self.data[0]))

    def test_calc_next_value(self):
        diff_tree = elftasks.calc_diff_tree(self.data[0])
        self.assertEqual(18, elftasks.calc_next_value(diff_tree))

    def test_calc_negative_diffs(self):
        data = "7 1 -5 0 28 99 260 616 1373 2893 5761 10864 19482 33391 54978 87368 134563 201593 294679 421408 590920"
        data = [int(x) for x in data.split(" ")]
        self.assertEqual([0] * 14, elftasks.calc_diff_tree(data)[-1])
