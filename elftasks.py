import string
import time
from collections import namedtuple
from collections import deque

from copy import deepcopy

from functools import partial

from operator import add
from operator import mul
from operator import sub
from operator import abs
from operator import floordiv
from operator import mod

import numpy
from numpy import sign



def day1():
    data = [line.strip().split() for line in open('input01.txt')]
    start_time = time.time()

    task1 = None
    task2 = None

    return time.time() - start_time, task1, task2
    