import elftasks
from datetime import date
import unittest


day_fn = """##############


def day{day}():
    data = [line.strip().split() for line in open('input{day}.txt')]
    start_time = time.time()

    task1 = None
    task2 = None

    return time.time() - start_time, task1, task2
    """

day_test_case = """###############


class TestDay{day}(unittest.TestCase):
    def test_task1(self):
        self.assertEqual(False, elftasks.day{day}())"""


def generate_day(file, fn_def, day):
    f = open(file, 'a')
    f.write("\n\n")
    f.write(fn_def.format(day=day))
    f.close()


def run(day):
    run_time, task1, task2 = day()
    print(day.__name__ + ": %.6s s - " % run_time + str(task1) + " " + str(task2))


def run_tests():
    suites = [unittest.defaultTestLoader.loadTestsFromName("test")]
    test_suite = unittest.TestSuite(suites)
    unittest.TextTestRunner().run(test_suite)


if __name__ == '__main__':
    run_tests()

    day = str(date.today().day)
    try:
        run(eval("elftasks.day" + day))
    except AttributeError:
        generate_day("elftasks.py", day_fn, day)
        generate_day("test.py", day_test_case, day)
