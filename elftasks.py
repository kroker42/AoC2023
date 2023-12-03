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
    return not ch.isdigit() and ch != '.'


def is_symbol_adjacent(row, cols, grid):
    row_range = (row - 1 if row > 0 else 0, row + 2 if row < len(grid) - 1 else row + 1)
    col_range = (cols[0] - 1 if cols[0] > 0 else 0, cols[1] + 1 if cols[1] < len(grid[0]) else cols[1])

    for r in range(row_range[0], row_range[1]):
        for c in range(col_range[0], col_range[1]):
            if is_symbol(grid[r][c]):
                return True
    return False


def find_numbers(grid):
    numbers = []
    for row in range(len(grid)):
        matches = re.finditer("[0-9]+", grid[row])
        for m in matches:
            if is_symbol_adjacent(row, m.span(), grid):
                numbers.append(int(grid[row][m.span()[0]:m.span()[1]]))
    return numbers


def day3():
    data = [line.strip() for line in open('input03.txt')]
    start_time = time.time()

    numbers = find_numbers(data)
    print(numbers)
    task1 = sum(numbers)
    task2 = None

    return time.time() - start_time, task1, task2
    