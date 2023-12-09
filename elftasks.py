import string
import time
import re
import numpy
import math
import operator
import sympy


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
    




