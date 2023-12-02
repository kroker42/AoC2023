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

def parse_hand(hand):
    marbles = dict.fromkeys(["red", "green", "blue"], 0)
    for s in hand:
        s = s.split(" ")
        marbles[s[-1]] = int(s[-2])

    return (marbles["red"], marbles["green"], marbles["blue"])

def min_bag(hand):
    return numpy.max(hand, axis=0)



def day2():
    data = [line.strip().split(":")[-1].split(";") for line in open('input02.txt')]

    start_time = time.time()

    games = []
    for game in data:
        games.append([])
        game = [hand.split(",") for hand in game]
        for hand in game:
            games[-1].append(parse_hand(hand))

    valid_games = []
    for i in range(len(games)):
        if validate_game(games[i]):
            valid_games.append(i+1)


    task1 = sum(valid_games)
    task2 = sum([numpy.prod(min_bag(hand)) for hand in games])

    return time.time() - start_time, task1, task2
    