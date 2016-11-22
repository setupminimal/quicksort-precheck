
from functools import partial

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

# Tests to see the total number of comparisons
# and swaps an algorithm needs for all of the
# lists of length n
def testN(f, n=9):
    return fold(plus, map(f, permutes(range(n))))

# Tests for all lists of length <= n
def test(f, n=9):
    x = lambda n: testN(f, n)
    return fold(plus, map(x, range(1, n+1)))

if __name__ == '__main__':
    n = 9
    print "Sorting Algorithm Benchmarking!"
    print
    print "Plain Quicksort:"
    x, y = 8226518, 7742058 #test(quicksort, n)
    print x, "-", y
    print
    print "Plain Insertion Sort:"
    x, y = 20750016, 7155322 #test(insertion, n)
    print x, "-", y
    print
    print "1st Sorted-ish Attempt - Beam guessing"
    print "Radius 1"
    x, y = 12237824, 7742057 #test(beam(1), n)
    print x, "-", y
    print "Radius 2"
    x, y = 11527898, 7742036 #test(beam(2), n)
    print x, "-", y
    print "Radius 3"
    x, y = 10220136, 7741510 #test(beam(3), n)
    print x, "-", y
    print
    print "Number of Pivots guessing"
    x, y = test(pivots, n)
    print x, "-", y
