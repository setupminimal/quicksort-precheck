
import multiprocessing as multi

# This partition function partitions in place,
# is unstable, and requires O(n) time.
def partition(array, lo, hi):
    split = lo # Tracks where the big + small things
    # are separated

    comparisons = hi - lo - 1
    swaps = 0

    pivot = array[lo]
    for i in xrange(lo + 1, hi):
        if array[i] < pivot:
            swaps += 1
            split += 1
            array[split], array[i] = array[i], array[split]

    # Swap the pivot into place
    swaps += 1
    array[lo], array[split] = array[split], array[lo]
    return split, comparisons, swaps

# Quicksort
# Written iterativly soas not to hit the
# recursion limit.
def quicksort(array, lo=0, hi=None):
    comparisons=0
    swaps=0
    if hi == None:
        hi = len(array)

    stack = [(lo, hi)]
    while stack != []:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        split, comps, swps = partition(array, lo, hi)
        comparisons += comps
        swaps += swps
        stack.append((lo, split))
        stack.append((split + 1, hi))
    return comparisons, swaps


# Insertion sort
def insertion(array):
    comparisons = 0
    swaps = 0
    for i in xrange(1, len(array)):
        b = i
        comparisons += 2
        while b > 0 and array[b] < array[b - 1]:
            swaps += 1
            array[b], array[b - 1] = array[b - 1], array[b]
            b -= 1
            comparisons += 2
    return comparisons, swaps


# Helper function that says whether an array
# is already sorted.
def sorted(l):
    comps = 0
    for i in xrange(len(l) - 1):
        comps += 1
        if l[i] > l[i+1]:
            return comps, False
    return comps, True
        
# This sorting algorithm does a single pass through the array,
# counts how many sections are in order
# and uses that to pick quicksort or insertion sort
def beam(radius):
    def sort(array):
        comparisons = 0
        orders = 0
        for i in xrange(radius, len(array) - radius):
            comps, t = sorted(array[i:i+(radius*2)+1])
            comparisons += comps
            if t:
                orders += 1
        if orders > len(array) - radius*2:
            comps, swaps = insertion(array)
        else:
            comps, swaps = quicksort(array)
        comparisons += comps
        return comparisons, swaps
    return sort

# This sorting algorithm attempts to guess the
# number of quicksort pivots, and chooses insertion
# sort if there are too many pivots
from math import log
def pivots(array):
    comparisons = 0
    max = min = array[0]
    pivots = 1
    for i in array:
        comparisons += 2
        if i < min:
            pivots += 1
            min = i
        if i > max:
            pivots += 1
            max = i
    if pivots > log(len(array), 2):
        comps, swaps = insertion(array)
    else:
        comps, swaps = quicksort(array)
    comparisons += comps
    return comparisons, swaps

# This generator returns all the permutations
# of length n lists.
def permutes(ar=range(9)):
    if len(ar) == 0:
        yield []
    for i in xrange(len(ar)):
        for l in permutes(ar[:i] + ar[i + 1:]):
            yield [ar[i]] + l


# Helper function to fold a list with an operation
def fold(o, l):
    acc = None
    for i in l:
        acc = o(acc, i)
    return acc

# Helper function for summing along tuples
def plus(a, b):
    if a is None:
        return b
    return (a[0] + b[0], a[1] + b[1])

# Check if quicksort performs more quickly than
# insertion sort for the given input
def quicksortQuicker(l):
    swapWeight = 10 # Assume swaps are 10 times more expensive
    a = l[:]
    b = l[:]
    comps, swaps = quicksort(a)
    comps2, swaps2 = insertion(b)
    return max(comps, swaps) < max(comps2, swaps2)

# Determine how many incorrect guesses f
# makes when determining if quicksort will be faster
def accuracyScore(f, n = 9):
    p=multi.Pool(processes=8)
    return sum(p.map(lambda l: 1 if f(l[:]) ^ quicksortQuicker(l) else 0, permutes(range(n))))


import time
#import matplotlib.pyplot as plt
def hlong(f, n):
    a = time.time()
    accuracyScore(f, n)
    return time.time() - a

##### GUESSING ENGINES

# This one guesses at random
import random
random.seed(0)
# Score: 165230
def rand(l):
    if random.randint(1, 3) == 1:
        return False
    return True

# This one checks if things are only getting more divergant
# Score: 135619
def diverge(l):
    max = min = l[0]
    changes = 0
    for i in l:
        if max < i:
            max = i
            changes += 1
        if min > i:
            min = i
            changes += 1
    return changes < len(l) - 2

def mul(a, b):
    if a is None:
        return b
    return a*b

def factorial(i):
    return fold(mul, range(1, i+1))

if __name__ == "__main__":
    with open("quicksort-results", "w") as f:
        for i in xrange(1,25):
            f.write(str(i) + " - " + str(accuracyScore(diverge, i)/float(factorial(i))) + " - " + str(accuracyScore(rand, i)/float(factorial(i))) + "\n")
            f.flush()
