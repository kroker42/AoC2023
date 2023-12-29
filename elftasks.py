import time
import re
import numpy
import math
import operator
import itertools

def match_digits(data):
    matches = {str(i): str(i) for i in range(1, 10)}
    matches["one"] = "1"
    matches["two"] = "2"
    matches["three"] = "3"
    matches["four"] = "4"
    matches["five"] = "5"
    matches["six"] = "6"
    matches["seven"] = "7"
    matches["eight"] = "8"
    matches["nine"] = "9"

    nums = []
    for l in data:
        nums.append([])
        i = 0
        while i < len(l):
            for digit in matches:
                new_i = 0
                x = re.findall("^" + digit, l[i:])
                if x:
                    nums[-1].append(matches[x[0]])
                    new_i = len(x[0])
                    break
            i += 1 if new_i <= 1 else new_i - 2
    return nums

def get_digits(data):
    return [[x for x in s if x.isdigit()] for s in data]


def day1():
    data = [line.strip() for line in open('input01.txt')]
    start_time = time.time()

    nums = [[x for x in i if x.isdigit()] for i in data]
    nums = [int(x[0] + x[-1]) for x in nums]
    task1 = sum(nums)

    nums = [int(x[0] + x[-1]) for x in match_digits(data)]
    task2 = sum(nums)

    return time.time() - start_time, task1, task2
    
###########

def validate_game(game):
    bag = (12, 13, 14)
    num = sum(bag)

    for hand in game:
        if numpy.greater(hand, bag).any() or sum(hand) > num:
            return False

    return True

def find_valid_games(games):
    """
    :param games: all game results
    :return: list of the 1-index-based ordinals of the valid games
    """
    valid_games = []
    for i in range(len(games)):
        if validate_game(games[i]):
            valid_games.append(i+1)
    return valid_games

def parse_hand(hand):
    """
    :param hand: a list containing space-separated strings, with a leading space.
     Each string contains info on how many marbles of a colour were pulled from the bag;
    in no specific order. 0-value colours are left out entirely.
    :return: a tuple representing the number of marbles for (red, green, blue)
    """
    marbles = dict.fromkeys(["red", "green", "blue"], 0)
    for s in hand:
        s = s.strip().split(" ")
        marbles[s[-1]] = int(s[-2])

    return tuple(marbles.values())  # using that dicts are ordered by keys


def day2():
    data = [line.strip().split(":")[-1].split(";") for line in open('input02.txt')]

    start_time = time.time()

    games = [[parse_hand(hand.split(",")) for hand in game] for game in data]

    task1 = sum(find_valid_games(games))
    task2 = sum([numpy.prod(numpy.max(hand, axis=0)) for hand in games])

    return time.time() - start_time, task1, task2
    

#####################################

def is_symbol(ch):
    """
    The grid contains numbers and symbols. Empty spots are marked by a dot.
    So symbols are neither numbers nor dots.
    """
    return not ch.isdigit() and ch != '.'


def get_bounding_box(row, col_span, grid_size):
    """
    Creates a bounding box for the given row and col span, taking care to not exceed the grid dimensions.
    The column span is a range, i.e. "736" in position 0 - 2 will have the span = (0,3)
    """
    row_range = range(row - 1 if row > 0 else 0, \
                      row + 2 if row < grid_size[0] - 1 else row + 1)
    col_range = range(col_span[0] - 1 if col_span[0] > 0 else 0, \
                      col_span[1] + 1 if col_span[1] < grid_size[1] else col_span[1])
    return (row_range, col_range)


def is_symbol_adjacent(row, cols, grid):
    """
    Checks if a number in the grid is next to a symbol, incl. diagonally.
    A number is identified by its row coordinate and its span over columns.
    The column span is a range, i.e. "736" in position 0 - 2 will have the span = (0,3)
    """
    bounding_box = get_bounding_box(row, cols, (len(grid), len(grid[0])))
    for r in bounding_box[0]:
        for c in bounding_box[1]:
            if is_symbol(grid[r][c]):
                return True
    return False


def find_number_matches(grid):
    """
    Finds all numbers in the grid, and their coordinates.
    Numbers are horizontal, so they have 1 row coordinate and span 1 or more columns.
    The column span is a range, i.e. "736" in position 0 - 2 will have the span = (0,3)
    """
    return [re.finditer("[0-9]+", grid[row]) for row in range(len(grid))]

def find_spare_parts(grid):
    """
    Spare parts are numbers that are next to a symbol in the grid, incl. diagonally.
    """
    numbers = []
    matches = find_number_matches(grid)
    for row in range(len(grid)):
        for m in matches[row]:
            cols = m.span()
            if is_symbol_adjacent(row, cols, grid):
                numbers.append(int(grid[row][cols[0]:cols[1]]))
    return numbers

def find_star_matches(grid):
    """
    Finds the coordinates of all star symbols in the grid
    """
    return [re.finditer("\*", grid[row]) for row in range(len(grid))]


def build_number_map(number_matches):
    """
    Creates a nested map of the coordinates of numbers in the map.
    map[row][col_span] = number
    The col_span is a range, i.e. "736" in position 0 - 2 will have the col_span = (0,3)
    """
    number_map = {row: {} for row in range(len(number_matches))}
    for row in range(len(number_matches)):
        number_map[row] = {m.span(): int(m.group(0)) for m in number_matches[row]}
    return number_map

def ranges_overlap(r1, r2):
    """
    Checks if 2 ranges overlap. Only works if the size of the ranges <= 3
    """
    return r1[0] in r2 or r1[1] - 1 in r2


def find_gears(grid):
    """
    Gears are star symbols adjacent to 2 spare parts.
    They are identified by the product of the spare part numbers.

    The algo uses that for every number, len(number) <= 3.
    It creates a bounding box for each star symbol, and checks if the start or end index of
    the number is inside the bounding box. If bigger numbers were allowed, this wouldn't work.
    """
    gears = []
    stars = find_star_matches(grid)
    numbers = build_number_map(find_number_matches(grid))

    for row in range(len(grid)):
        for star_match in stars[row]:
            adjacent_nums = []

            box = get_bounding_box(row, star_match.span(), (len(grid), len(grid[0])))
            for row in box[0]:
                adjacent_nums += [numbers[row][cols] for cols in numbers[row] if ranges_overlap(cols, box[1])]

            if len(adjacent_nums) > 1:
                gears.append(numpy.prod(adjacent_nums))

    return gears


def day3():
    data = [line.strip() for line in open('input03.txt')]
    start_time = time.time()

    numbers = find_spare_parts(data)
    task1 = sum(numbers)

    gears = find_gears(data)
    task2 = sum(gears)

    return time.time() - start_time, task1, task2


##############


def day4():
    """
    Count wins on scratch cards. A card has a set of winning numbers and a set of numbers.
    """
    data = [line.strip().split(':')[-1] for line in open('input04.txt')]

    start_time = time.time()

    win_count = []
    for card in data:
        [wins, numbers] = [{int(i) for i in x.split(' ') if i.isdigit()} for x in card.split('|')]
        win_count.append(len(wins.intersection(numbers)))

    points = [2 ** (i - 1) for i in win_count if i > 0]
    task1 = sum(points)

    card_count = {i: 1 for i in range(len(data))}
    for i in range(len(card_count)):
        for win in range(1, win_count[i] + 1):
            card_count[i+win] += card_count[i]

    task2 = sum(card_count.values())

    return time.time() - start_time, task1, task2

##############

def parse_seeds(s):
    data = s.split(':')
    return [int(x) for x in data[-1].strip().split(' ')]

def parse_dest_map(data, start):
    i = start
    result = {}
    while data[i]:  # map data ends with an empty line
        val, key, length = [int(x) for x in data[i].strip().split(' ')]
        result[range(key, key + length)] = val
        i += 1
    return i, result

def parse_dest_maps(data):
    """
    Input contains mapping information for a 7-long chain of locations for the seeds.
    The maps are separated by a blank line, and preceded by a description line.
    The first line of data contain seed info and not a map, so we start parsing at line 3.
    """
    maps = [''] * 7
    next_i = 1
    for i in range(7):
        next_i, maps[i] = parse_dest_map(data, next_i + 2)
    return maps


def parse_seed_ranges(seeds):
    return [range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds) - 1, 2)]

def get_next_destinations(sources, dest_map):
    destinations = []
    for source in sources:
        dest = source
        for key in dest_map.keys():
            if source in key:
                dest = dest_map[key] + (source - key.start)
        destinations.append(dest)
    return destinations


def get_next_destination_ranges(source_ranges, dest_map):
    destinations = []
    sources = source_ranges.copy()
    for source in sources:
        found = False
        for key in dest_map.keys():
            if source.start in key:  # dest range contains start of source range
                dest = dest_map[key] + (source.start - key.start)
                stop = min(key.stop, source.stop)
                destinations.append(range(dest, dest + (stop - source.start)))

                if key.stop < source.stop:  # source range continues past end of key range
                    sources.append(range(key.stop, source.stop))  # check the end of the source range
                found = True
                break
            elif key.start in source:  # key range contains middle or end of source range
                dest = dest_map[key]
                stop = min(key.stop, source.stop)
                destinations.append(range(dest, dest + (stop - key.start)))

                # check the start of the source range
                sources.append(range(source.start, key.start))

                if key.stop < source.stop:  # source range contains key range, check end of source range
                    sources.append(range(key.stop, source.stop))
                found = True
                break
        if not found:  # if there's no mapping, dest range == source range
            destinations.append(source)

    return destinations


def day5():
    inp = open('input05.txt')
    data = inp.read()
    inp.close()
    data = data.split('\n')

    start_time = time.time()

    seeds = parse_seeds(data[0])
    maps = parse_dest_maps(data)

    destinations = seeds
    for dest_map in maps:
        destinations = get_next_destinations(destinations, dest_map)

    task1 = min(destinations)

    dest_ranges = parse_seed_ranges(seeds)
    for dest_map in maps:
        dest_ranges = get_next_destination_ranges(dest_ranges, dest_map)

    task2 = min([r.start for r in dest_ranges])

    return time.time() - start_time, task1, task2

##############


def day6():
    data = [line.strip().split(':')[-1].split(' ') for line in open('input06.txt')]

    start_time = time.time()

    times, distances = [[int(x) for x in line if x.isdigit()] for line in data]
    races = zip(times, distances)

    options = []
    for race in races:
        wins = []
        for t in range(race[0]):
            dist = (race[0] - t) * t
            if dist > race[1]:
                wins.append(dist)
        options.append(len(wins))

    task1 = math.prod(options)

    race_time, distance = [int("".join([x for x in line if x])) for line in data]

    x = 0
    while (race_time - x) * x < distance:
        x += 1

    y = race_time
    while (race_time - y) * y < distance:
        y -= 1

    task2 = y - x + 1

    return time.time() - start_time, task1, task2

##############

def parse_hand(hand):
    card_vals = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    return [card_vals[card] if card in card_vals else int(card) for card in hand]

def score_hand(hand):
    counts = {}
    for card in hand:
        counts[card] = counts[card] + 1 if card in counts else 1

    unique_cards = list(counts.values())
    unique_cards.sort(reverse=True)
    return unique_cards

def parse_joker_hand(hand):
    card_vals = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10}
    return [card_vals[card] if card in card_vals else int(card) for card in hand]

def score_joker_hand(hand):
    score = score_hand(hand)
    joker_count = hand.count(1)
    joker_score = []
    if joker_count == 5:
        joker_score = score
    else:
        score.remove(joker_count)
        joker_score = [score[0] + joker_count] + score[1:]

    return joker_score


def day7():
    data = [line.strip().split(" ") for line in open('input07.txt')]

    start_time = time.time()

    hands = [(parse_hand(player[0]), int(player[1])) for player in data]

    scores = {}
    for hand in hands:
        score = score_hand(hand[0])
        if score in scores:
            scores[score].append(hand)
        else:
            scores[score] = [hand]

    multiplier = 1
    task1 = 0
    for score in scores.values():
        score.sort(key=operator.itemgetter(0))  # ascending lexicographical sort of hand
        for hand in score:
            task1 += multiplier * hand[1]
            multiplier += 1

    joker_hands = [(parse_joker_hand(player[0]), int(player[1])) for player in data]

    joker_scores = {}
    for hand in joker_hands:
        score = score_joker_hand(hand[0])
        if score in scores:
            joker_scores[score].append(hand)
        else:
            joker_scores[score] = [hand]

    multiplier = 1
    task2 = 0
    for score in joker_scores.values():
        score.sort(key=operator.itemgetter(0))  # ascending lexicographical sort of hand
        for hand in score:
            task2 += multiplier * hand[1]
            multiplier += 1

    return time.time() - start_time, task1, task2

##############

def parse_desert_map(data):
    """JKT = (KFV, CFQ)"""
    return data[0:3], data[7:10], data[12:15]

def locs_at_Z(locs):
    for loc in locs:
        if loc[-1] != 'Z':
            return False
    return True

def find_cycle(start, path, desert_map):
    step = 0
    loc = start
    path_len = len(path)
    while True:
        if loc[-1] == 'Z':
            return (loc, step)
        loc = desert_map[loc][0] if path[step % path_len] == 'L' else desert_map[loc][1]
        step += 1


def day8():
    data = [line.strip() for line in open('input08.txt')]

    start_time = time.time()

    path = data[0]
    desert_map = {}
    for instr in data[2:]:
        key, left, right = parse_desert_map(instr)
        desert_map[key] = (left, right)

    path_len = len(path)

    loc = 'AAA'
    step = 0
    while loc != 'ZZZ':
        loc = desert_map[loc][0] if path[step % path_len] == 'L' else desert_map[loc][1]
        step += 1

    task1 = step

    locs = [loc for loc in desert_map if loc[-1] == 'A']
    cycles = [find_cycle(loc, path, desert_map) for loc in locs]
    # examining the cycles, we discover that they are all == a prime number * path_len
    prime_factors = [cycle[1] // path_len for cycle in cycles]
    task2 = math.prod(prime_factors) * path_len

    return time.time() - start_time, task1, task2
    

##############

def calc_diffs(reading):
    return [j - i for i, j in zip(reading[:-1], reading[1:])]


def calc_diff_tree(reading):
    diffs = [reading]
    while 1 < len(diffs[-1]) != diffs[-1].count(0):
        diffs.append(calc_diffs(diffs[-1]))

    return diffs


def calc_next_value(diff_tree):
    next_value = 0
    for diffs in reversed(diff_tree[:-1]):
        next_value += diffs[-1]

    return next_value


def calc_prev_value(diff_tree):
    prev_value = 0
    for diffs in reversed(diff_tree[:-1]):
        prev_value = diffs[0] - prev_value

    return prev_value


def day9():
    data = [[int(x) for x in line.strip().split(" ")] for line in open('input09.txt')]
    start_time = time.time()

    diff_trees = [calc_diff_tree(reading) for reading in data]

    task1 = sum([calc_next_value(diff_tree) for diff_tree in diff_trees])
    task2 = sum([calc_prev_value(diff_tree) for diff_tree in diff_trees])

    return time.time() - start_time, task1, task2

##############

def find_start(pipe_map):
    for row in range(len(pipe_map)):
        for col in range(len(pipe_map[0])):
            if pipe_map[row][col] == 'S':
                return row, col


def valid_coords(point, pipe_map):
    return min(point) >= 0 and point[0] < len(pipe_map) and point[1] < len(pipe_map[0])


def find_start_connections(point, pipe_map):
    compass = {(0, -1): ['-', 'F', 'L'], (0, 1): ['-', 'J', '7'], (-1, 0): ['|', 'F', '7'], (1, 0): ['|', 'L', 'J']}

    neighbours = []
    for n in compass:
        n_c = numpy.add(point, n)
        if valid_coords(n_c, pipe_map) and pipe_map[n_c[0]][n_c[1]] in compass[n]:
            neighbours.append(tuple(n_c))

    return neighbours

def find_connected_neighbours(point, pipe_map):

    neighbour_directions = {'-': [(0, -1), (0, 1)], '|': [(-1, 0), (1, 0)],
                            'F': [(1, 0), (0, 1)], 'L': [(-1, 0), (0, 1)],
                            'J': [(0, -1), (-1, 0)], '7': [(0, -1), (1, 0)]}

    neighbours = []
    for n in neighbour_directions[pipe_map[point[0]][point[1]]]:
        n_c = numpy.add(point, n)
        if valid_coords(n_c, pipe_map):
            neighbours.append(tuple(n_c))
    return neighbours


def find_loop(start, pipe_map):
    distances = {start: 0}
    pipes = find_start_connections(start, pipe_map)
    for neighbour in pipes:
        distances[neighbour] = 1

    while len(pipes):
        current = pipes.pop(0)
        neighbours = find_connected_neighbours(current, pipe_map)
        for neighbour in neighbours:
            if neighbour not in distances:
                distances[neighbour] = distances[current] + 1
                pipes.append(neighbour)

    return distances


def is_vertical_kinked_edge(row, col, pipe_map, polygon_points):
    """
    The special case when a vertical edge goes up(down), turns right for a bit, then continues up(down) -
    that's essentially the same vertical edge, and counts as on continuous edge (with a horizontal kink).
    E.g. 'F--J' counts as one edge, or 'L-7'
    """
    corner = pipe_map[row][col]

    if corner in ['F', 'L']:
        while True:
            col += 1
            if pipe_map[row][col] != '-':
                break
        return (corner == 'F' and pipe_map[row][col] == 'J') or (corner == 'L' and pipe_map[row][col] == '7')

    return False


def ray_cast(pipe_map, polygon_points):
    """
    Finding all points inside a polygon can be solved by casting a ray through the polygon.
    All points encountered before the first edge are outside the polygon. All points before the next edge are inside,
    then outside to the next edge, then inside to the next edge, etc.

    This problem is simplified because all corners are 90 degree angles, so all edges are vertical or horizontal.
    It means we only need to cast rays e.g. horizontally, and only take into account vertical edges.

    Any points on edges are a special case and considered outside.
    Since horizontal edges count as outside, they (incl. corners) don't affect a ray shone along it -
    points to left of the horizontal edge and to the right of it are all on the outside.

    Except for the special case when a vertical edge goes up(down), turns right for a bit, then continues up(down) -
    that's essentially the same vertical edge, and counts as on continuous edge (with a horizontal kink).
    E.g. 'F--J' counts as one edge, or 'L-7'

    So we find all vertical edges, excl. their start and stop corner, shine horizontal rays through them
    from left to right, and count any points that are between pairs of vertical edges.

    Vertical edges are marked by a '|' symbol in the matrix, and are included as keys in the distance map -
    we can either trace through the whole polygon shape again and find them, or just find all in the matrix and
    check if they're included as keys in the distance map from task 1.
    """
    inside = 0
    for row in range(len(pipe_map)):
        edge_count = 0
        for col in range(len(pipe_map[0])):
            if (row, col) not in polygon_points:
                inside += edge_count % 2  # only count points between an edge pait, i.e. we've seen an uneven no. of edges
            elif pipe_map[row][col] == '|' or is_vertical_kinked_edge(row, col, pipe_map, polygon_points):
                edge_count += 1  # if it's on the polygon edge and a vertical edge - count it

    return inside



def day10():
    pipe_map = [line.strip() for line in open('input10.txt')]
    start_time = time.time()

    map_dims = (len(pipe_map), len(pipe_map[0]))

    start = find_start(pipe_map)
    distances = find_loop(start, pipe_map)
    task1 = max(distances.values())

    # hack - my start position should be an 'F' pipe - it affects the kinked vertical edge analysis...
    # not exactly a sustainable piece of coding, this.
    pipe_map[start[0]] = pipe_map[start[0]][:start[1]] + 'F' + pipe_map[start[0]][start[1] + 1:]
    task2 = ray_cast(pipe_map, distances)

    return time.time() - start_time, task1, task2

##############


def parse_galaxies(data):
    galaxies = []
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == '#':
                galaxies.append([row, col])
    return galaxies


def find_empty_rows(data):
    empty_rows = []
    for row in range(len(data)):
        if data[row].count('#') == 0:
            empty_rows.append(row)
    return empty_rows


def find_empty_cols(data):
    empty_cols = []
    for col in range(len(data[0])):
        empty = True
        for row in range(len(data)):
            empty = data[row][col] != '#'
            if not empty:
                break
        if empty:
            empty_cols.append(col)
    return empty_cols


def pad_galaxies(galaxies, empty_rows, empty_cols, factor=2):
    padded_galaxies = [g.copy() for g in galaxies]

    for row in reversed(empty_rows):
        for g in padded_galaxies:
            if g[0] > row:
                g[0] += factor - 1

    for col in reversed(empty_cols):
        for g in padded_galaxies:
            if g[1] > col:
                g[1] += factor - 1

    return padded_galaxies


def get_distances(galaxies):
    galaxy_pairs = itertools.combinations(galaxies, 2)
    distances = [sum([abs(i) for i in numpy.subtract(p[0], p[1])]) for p in galaxy_pairs]
    return distances


def day11():
    data = [line.strip() for line in open('input11.txt')]
    start_time = time.time()

    galaxies = parse_galaxies(data)
    empty_rows = find_empty_rows(data)
    empty_cols = find_empty_cols(data)

    task1 = sum(get_distances(pad_galaxies(galaxies, empty_rows, empty_cols)))
    task2 = sum(get_distances(pad_galaxies(galaxies, empty_rows, empty_cols, 1000000)))

    return time.time() - start_time, task1, task2
    

##############

def find_unsmudged_mirror(data):
    for i in range(len(data) - 1):
        if (data[i] == data[i + 1]).all():
            match = True
            sz = min(i, len(data) - (i + 2))
            for j in range(sz):
                if not (data[i - 1 - j] == data[i + 2 + j]).all():
                    match = False
                    break
            if match:
                return i + 1
    return 0

def find_smudged_mirror(data):
    for i in range(len(data) - 1):
        if (data[i] == data[i + 1]).all():
            match = True
            sz = min(i, len(data) - (i + 2))
            for j in range(sz):
                if (data[i - 1 - j] == data[i + 2 + j]).count_nonzero() < len(data[0]):
                    match = False
                    break
            if match:
                return i + 1
    return 0


def day13():
    inp = open('input13.txt')
    data = inp.read()
    inp.close()
    data = data.split('\n')

    delims = [-1] + [i for i in range(len(data)) if data[i] == '']
    patterns = [numpy.array([list(row) for row in data[i + 1: j]]) for i, j in zip(delims[:-1], delims[1:])]

    start_time = time.time()

    horizontal_mirrors = [find_unsmudged_mirror(pattern) for pattern in patterns]
    vertical_mirrors = [find_unsmudged_mirror(pattern.T) for pattern in patterns]

    task1 = 100 * sum(horizontal_mirrors) + sum(vertical_mirrors)
    task2 = None

    return time.time() - start_time, task1, task2


##############

def tilt_rocks_north(platform):
    """Changes the platform array"""

    for col in range(len(platform[0])):
        for row in range(1, len(platform)):
            if platform[row][col] == 'O':
                for prev_row in reversed(range(row)):
                    if platform[prev_row][col] == '.':
                        platform[prev_row][col] = 'O'
                        platform[prev_row + 1][col] = '.'
                    else:
                        break
    return platform

def calc_load(platform):
    weight = len(platform)
    load = 0
    for i in range(len(platform)):
        load += numpy.count_nonzero(platform[i] == 'O') * (weight - i)
    return load

def rotate_and_tilt(platform):
    """ Tilt platform in N, W, S, E directions in turn, by rotating the array and tilting it."""
    tilt_rocks_north(platform)
    tilt_rocks_north(platform.T)
    tilt_rocks_north(numpy.flip(platform, 0))
    tilt_rocks_north(numpy.flip(platform.T, 0))


def day14():
    data = [line.strip('\n') for line in open('input14.txt')]
    platform = numpy.array([list(row) for row in data])

    start_time = time.time()

    task1 = calc_load(tilt_rocks_north(platform.copy()))

    # the cycle is 77 rotations long
    cycle_part = [86096,86085,86079,86071,86064,86082,86100,86106]
    loads = [0] * 10000

    for i in range(500):
        rotate_and_tilt(platform)

    for i in range(500, 10000):
        rotate_and_tilt(platform)
        loads[i] = calc_load(platform)
        if loads[i-7:i+1] == cycle_part:
            break
    print(loads[500:600])

    task2 = calc_load(platform)

    return time.time() - start_time, task1, task2



##############

def hash(str):
    hash_value = 0
    for ch in str:
        hash_value += ord(ch)
        hash_value = (hash_value * 17) % 256
    return hash_value


def parse_lens_instruction(instr):
    if instr[-1] == '-':
        return (instr[:-1], None)
    else:
        return (instr[:-2], int(instr[-1]))


def arrange_lenses(instructions):
    lenses = [{} for i in range(256)]
    for instr in instructions:
        label = parse_lens_instruction(instr)
        hash_val = hash(label[0])
        if label[1] == None:
            lenses[hash_val].pop(label[0], None)
        else:
            lenses[hash_val][label[0]] = label[1]
    return lenses


def day15():
    inp = open('input15.txt')
    data = inp.read()
    inp.close()
    data = data.strip().split(',')

    start_time = time.time()

    task1 = sum([hash(x) for x in data])

    boxes = arrange_lenses(data)

    focus_powers = 0
    for i in range(256):
        lenses = list(boxes[i].values())
        for l in range(len(lenses)):
            focus_powers += (i + 1) * (l + 1) * lenses[l]

    task2 = focus_powers

    return time.time() - start_time, task1, task2
    

##############

def bounce_beam(mirrors):
    energised = {(0, 0): 1}
    next = [(0, 1)]
    for beam in next:
        Non




def day16():
    data = [line.strip() for line in open('input16.txt')]
    start_time = time.time()

    task1 = None
    task2 = None

    return time.time() - start_time, task1, task2
    

##############

class Node:
    def __init__(self, index, value, prev_node=None):
        self.index = index
        self.prev_node = prev_node
        if prev_node:
            self.path_length = value + prev_node.path_length
            self.prev_direction = numpy.subtract(self.index, self.prev_node.index)
            self.step = prev_node.step + 1 if numpy.equal(self.prev_direction, prev_node.prev_direction).all() else 1
            self.prev_indices = {tuple(self.prev_node.index)}.union(self.prev_node.prev_indices)
        else:
            self.path_length = value
            self.prev_direction = (0, 0)
            self.step = 0
            self.prev_indices = set()

    def visited(self, index):
        return tuple(index) in self.prev_indices


class Paths:
    def __init__(self, grid):
        self.grid = grid
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.paths = {}
        self.encountered_nodes = {}
        self.paths_to_target = []

    def add_path(self, node):
        estimated_path_length = node.path_length

        # if a different path has a shorter length to this node - stop here
        node_index = tuple(node.index)
        if node_index not in self.encountered_nodes:
            self.encountered_nodes[node_index] = {}

        prev_direction = tuple(node.prev_direction)
        if prev_direction in self.encountered_nodes[node_index]:
            for path in self.encountered_nodes[node_index][prev_direction]:
                if path.step <= node.step and path.path_length <= node.path_length:
                    return
        else:
            self.encountered_nodes[node_index][prev_direction] = []

        if estimated_path_length not in self.paths:
            self.paths[estimated_path_length] = []

        self.paths[estimated_path_length].append(node)
        self.encountered_nodes[node_index][prev_direction].append(node)

    def add_ultra_path(self, node):
        estimated_path_length = node.path_length

        # if a different path has a shorter length to this node - stop here
        node_index = tuple(node.index)
        if node_index not in self.encountered_nodes:
            self.encountered_nodes[node_index] = {}

        prev_direction = tuple(node.prev_direction)
        if prev_direction not in self.encountered_nodes[node_index]:
            self.encountered_nodes[node_index][prev_direction] = []
        else:
            for path in self.encountered_nodes[node_index][prev_direction]:
                if path.step == node.step and path.path_length <= node.path_length:
                    return

        if estimated_path_length not in self.paths:
            self.paths[estimated_path_length] = []

        self.paths[estimated_path_length].append(node)
        self.encountered_nodes[node_index][prev_direction].append(node)

    def in_grid(self, coords):
        return numpy.greater_equal(coords, (0, 0)).all() and \
                not numpy.greater_equal(coords, (self.num_rows, self.num_cols)).any()

    def possible_directions(self, node):
        """
        It's possible to turn 90 degrees in either direction, or continue straight on, but only for 3 steps.
        It's not possible to turn around or walk diagonally.
        It's not possible to walk outside the grid.
        """

        # 90-degree turns
        candidates = [numpy.flip(node.prev_direction),
                      -numpy.flip(node.prev_direction)]

        # continue straight
        if node.step < 3:
            candidates.append(node.prev_direction)

        return [x for x in candidates if
                self.in_grid(numpy.add(node.index, x)) and not node.visited(numpy.add(node.index, x))]

    def possible_ultra_directions(self, node):
        """
        An ultra crucible *must* walk a minimum of 4 steps in a straight line.
        It cannot walk more than 10 steps in one direction.
        """

        candidates = []

        # 90-degree turns
        if 4 <= node.step <= 10:
            candidates = [numpy.flip(node.prev_direction),
                          -numpy.flip(node.prev_direction)]

        # continue straight
        if node.step < 10:
            candidates.append(node.prev_direction)

        return [x for x in candidates if
                self.in_grid(numpy.add(node.index, x)) and not node.visited(numpy.add(node.index, x))]

    def is_origin(self, node):
        return numpy.equal(node.index, (0, 0)).all()

    def is_target(self, node):
        return numpy.equal(node.index, (self.num_rows - 1, self.num_cols - 1)).all()

    def create_new_paths(self, path):
        coords = [numpy.add(path.index, direction) for direction in self.possible_directions(path)]
        return [Node(index, self.grid[index[0]][index[1]], path) for index in coords]

    def create_new_ultra_paths(self, path):
        coords = [numpy.add(path.index, direction) for direction in self.possible_ultra_directions(path)]
        return [Node(index, self.grid[index[0]][index[1]], path) for index in coords]

    def get_shortest_estimated_path(self):
        shortest_estimated_path_len = min(self.paths.keys())
        path = self.paths[shortest_estimated_path_len].pop(-1)

        if not self.paths[shortest_estimated_path_len]:
            self.paths.pop(shortest_estimated_path_len)

        return path

    def find_shortest_path(self):
        """
        find shortest path from top left to bottom right corner; using no more than 3 steps in a straight line.
        don't count the number in the starting position.
        """

        src = Node((0, 0), 0)

        self.add_path(Node((0, 1), self.grid[0][1], src))
        self.add_path(Node((1, 0), self.grid[1][0], src))

        while self.paths:
            path = self.get_shortest_estimated_path()
            new_paths = self.create_new_paths(path)

            for new_path in new_paths:
                if self.is_target(new_path):
                    self.paths_to_target.append(new_path)
                else:
                    self.add_path(new_path)

        shortest = self.paths_to_target[0]
        for path in self.paths_to_target:
            if path.path_length < shortest.path_length:
                shortest = path

        return shortest

    def find_shortest_ultra_path(self):
        """
        find shortest path from top left to bottom right corner;
        using no less than 4 and no more than 10 steps in a straight line.
        don't count the number in the starting position.
        """

        src = Node((0, 0), 0)

        self.add_ultra_path(Node((0, 1), self.grid[0][1], src))
        self.add_ultra_path(Node((1, 0), self.grid[1][0], src))

        while self.paths:
            path = self.get_shortest_estimated_path()
            new_paths = self.create_new_ultra_paths(path)

            for new_path in new_paths:
                if self.is_target(new_path):
                    self.paths_to_target.append(new_path)
                else:
                    self.add_ultra_path(new_path)

        return self.paths_to_target

def day17():
    data = [[int(x) for x in line.strip()] for line in open('input17.txt')]
    start_time = time.time()

    # shortest_path = Paths(data).find_shortest_path()
    # task1 = shortest_path.path_length

    shortest_paths = Paths(data).find_shortest_ultra_path()
    shortest_paths = [path for path in shortest_paths if path.step >= 4]

    shortest = shortest_paths[0].path_length
    for path in shortest_paths:
        if path.path_length < shortest:
            shortest = path.path_length

    task2 = shortest

    return time.time() - start_time, None, task2
    

##############


