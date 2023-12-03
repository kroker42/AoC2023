import string
import time
import re
import numpy

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
