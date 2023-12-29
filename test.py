import unittest
import elftasks
import numpy

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


###############


class TestDay10(unittest.TestCase):
    def test_valid_point(self):
        data = """.....
.S-7.
.|.|.
.L-J.
....."""
        pipe_map = data.split('\n')
        self.assertEqual(True, elftasks.valid_coords((1,1), pipe_map))
        self.assertEqual(True, elftasks.valid_coords((1,1), pipe_map))
        self.assertEqual(True, elftasks.valid_coords((1,4), pipe_map))
        self.assertEqual(False, elftasks.valid_coords((-1,1), pipe_map))
        self.assertEqual(False, elftasks.valid_coords((5,1), pipe_map))

    def test_task1(self):
        data = """.....
.S-7.
.|.|.
.L-J.
....."""
        pipe_map = data.split('\n')
        start = elftasks.find_start(pipe_map)
        distances = elftasks.find_loop(start, pipe_map)
        self.assertEqual(4, max(distances.values()))

    def test_ray_cast(self):
        data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
        pipe_map = data.split('\n')
        start = elftasks.find_start(pipe_map)
        distances = elftasks.find_loop(start, pipe_map)
        self.assertEqual(10, elftasks.ray_cast(pipe_map, distances))



###############


class TestDay11(unittest.TestCase):
    def test_task1(self):
        data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
        data = data.split('\n')
        galaxies = elftasks.parse_galaxies(data)
        empty_rows = elftasks.find_empty_rows(data)
        empty_cols = elftasks.find_empty_cols(data)

        small_galaxies = elftasks.pad_galaxies(galaxies, empty_rows, empty_cols)

        self.assertEqual(True, [6, 1] in small_galaxies)
        self.assertEqual(True, [7, 12] in small_galaxies)

        distances = elftasks.get_distances(small_galaxies)
        self.assertEqual(374, sum(distances))

        big_galaxies = elftasks.pad_galaxies(galaxies, empty_rows, empty_cols, 10)
        self.assertEqual(1030, sum(elftasks.get_distances(big_galaxies)))

        bigger_galaxies = elftasks.pad_galaxies(galaxies, empty_rows, empty_cols, 100)
        self.assertEqual(8410, sum(elftasks.get_distances(bigger_galaxies)))


###############


class TestDay13(unittest.TestCase):
    def test_unsmudged_mirror(self):
        data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        pattern = numpy.array([list(row) for row in data.split('\n')])
        self.assertEqual(0, elftasks.find_unsmudged_mirror(pattern))

        data = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        pattern = numpy.array([list(row) for row in data.split('\n')])
        self.assertEqual(4, elftasks.find_unsmudged_mirror(pattern))



###############


class TestDay14(unittest.TestCase):
    def test_task1(self):
        data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
        platform = numpy.array([list(row) for row in data.split('\n')])
        tilted_data = numpy.array([list(row) for row in """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....""".split('\n')])
        tilted_platform = elftasks.tilt_rocks_north(platform.copy())
        self.assertTrue((tilted_platform == tilted_data).all())
        self.assertEqual(136, elftasks.calc_load(tilted_platform))

        for i in range(10):
            elftasks.rotate_and_tilt(platform)


###############


class TestDay1(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(52, elftasks.hash("HASH"))

        data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')
        self.assertEqual(1320, sum([elftasks.hash(x) for x in data]))

        self.assertEqual(0, elftasks.hash("rn"))

    def test_arrange_lenses(self):
        data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')
        lenses = elftasks.arrange_lenses(data)
        self.assertEqual({'rn': 1, 'cm': 2}, lenses[0])
        self.assertEqual({'ot': 7, 'ab': 5, 'pc': 6}, lenses[3])






###############


class TestDay16(unittest.TestCase):
    def test_task1(self):
        self.assertEqual(False, False)

###############


class TestDay17(unittest.TestCase):
    data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split('\n')
    data = [[int(x) for x in line] for line in data]

    def test_finds_coords_within_grid(self):
        paths = elftasks.Paths(self.data)

        self.assertTrue(paths.in_grid((0, 0)))
        self.assertTrue(paths.in_grid((0, 1)))
        self.assertTrue(paths.in_grid((1, 1)))
        self.assertTrue(paths.in_grid((12, 12)))
        self.assertTrue(paths.in_grid((12, 11)))

        self.assertFalse(paths.in_grid((12, 13)))
        self.assertFalse(paths.in_grid((13, 12)))
        self.assertFalse(paths.in_grid((12, -1)))
        self.assertFalse(paths.in_grid((-1, 12)))
        self.assertFalse(paths.in_grid((0, -1)))
        self.assertFalse(paths.in_grid((-1, 0)))


    def test_find_possible_directions_from_node(self):
        paths = elftasks.Paths(self.data)

        node = elftasks.Node((3, 4), 2, elftasks.Node((4, 4), 5))
        self.assertEqual(1, node.step)
        directions = paths.possible_directions(node)
        self.assertTrue(numpy.equal([(0, -1), (0, 1), (-1, 0)], directions).all())

        nodeN = elftasks.Node((2, 4), 2, node)
        self.assertEqual(2, nodeN.step)
        self.assertTrue(numpy.equal([(0, -1), (0, 1), (-1, 0)], paths.possible_directions(nodeN)).all())

        nodeW = elftasks.Node((3, 3), 2, node)
        self.assertEqual(1, nodeW.step)
        self.assertTrue(numpy.equal([(-1, 0), (1, 0), (0, -1)], paths.possible_directions(nodeW)).all())

        nodeWW = elftasks.Node((3, 2), 2, nodeW)
        self.assertEqual(2, nodeWW.step)
        self.assertTrue(numpy.equal([(-1, 0), (1, 0), (0, -1)], paths.possible_directions(nodeWW)).all())

        nodeWWW = elftasks.Node((3, 1), 2, nodeWW)
        self.assertEqual(3, nodeWWW.step)
        self.assertTrue(numpy.equal([(-1, 0), (1, 0)], paths.possible_directions(nodeWWW)).all())

    def test_find_possible_directions_from_edge_node(self):
        paths = elftasks.Paths(self.data)
        node = elftasks.Node((12, 2), 2, elftasks.Node((11, 2), 5))
        self.assertEqual(1, node.step)
        self.assertTrue(numpy.equal([(0, 1), (0, -1)], paths.possible_directions(node)).all())

        node = elftasks.Node((12, 0), 2, elftasks.Node((11, 0), 5))
        self.assertEqual(1, node.step)
        self.assertTrue(numpy.equal([(0, 1)], paths.possible_directions(node)).all())

    def test_is_origin(self):
        paths = elftasks.Paths(self.data)
        self.assertTrue(paths.is_origin(elftasks.Node((0, 0), 2)))
        self.assertFalse(paths.is_origin(elftasks.Node((0, 1), 2)))

    def test_find_shortest_path(self):
        paths = elftasks.Paths(self.data)
        shortest_path = paths.find_shortest_path()
        self.assertEqual(102, shortest_path.path_length)

    def test_find_shortest_ultra_path(self):
        paths = elftasks.Paths(self.data)
        shortest_paths = paths.find_shortest_ultra_path()

        shortest = shortest_paths[0].path_length
        for path in shortest_paths:
            if path.path_length < shortest:
                shortest = path.path_length

        self.assertEqual(94, shortest)

    def test_find_ultra_path_small_map(self):
        data = """111111111111
999999999991
999999999991
999999999991
999999999991""".split('\n')
        data = [[int(x) for x in line] for line in data]
        paths = elftasks.Paths(data)
        shortest_paths = paths.find_shortest_ultra_path()
        shortest_paths = [path for path in shortest_paths if path.step >= 4]

        shortest = shortest_paths[0].path_length
        for path in shortest_paths:
            if path.path_length < shortest:
                shortest = path.path_length

        self.assertEqual(71, shortest)

