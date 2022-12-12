"""Binary heap with ability to delete elements (on the top of "heapq" module)

Usage:

- initialisation: H = DeletableMinHeap()  [similar for MaxHeap]

- add element x: H.push(x)

- pop minimal element: H.pop()

- retrieve minimal element without pop (breaks if H empty): H.min()

- delete element x (breaks down if x not there): H.delete(x)

- test if x in H: x in H

Algorithm:

- The idea is to also have a dictionary, counting the occurences
of each element in the heap, in addition to the heap.

- Deletion is trivial: simply decrease the counter of the deleted element;
notice that the heap doesn't match the dictionary after a deletion;
the dictionary is the truth

- We must correct the interaction between the two structures:
each time we have to extract the minumum or to pop, we must correct the heap
(by popping all elements in the heap which are already deleted from the
dictionary); note that deletion is then O(1)
(two operations, one in the "delete" function, and (at most) one correction
in minimum/pop)

- Note the dictionary is at any point more up to date than the heap

Note: I also included a MaxHeap for convenience
(by simply working with a MinHeap of opposites)

Source: from user Kiri8128 at AtCoder

Tested: on ABC 281, problem E (AtCoder)
"""

from collections import defaultdict
from heapq import heappush, heappop


class DeletableMinHeap:
    def __init__(self):
        self.heap = []
        self.counter = defaultdict(int)

    def __contains__(self, x):
        if (x in self.counter) and (self.counter[x] > 0):
            return True
        else:
            return False

    def push(self, x):
        heappush(self.heap, x)
        self.counter[x] += 1

    def delete(self, x):
        # it breaks down (intentioanlly) if x not in the structure
        assert self.counter[x] > 0
        self.counter[x] -= 1
        # note that the heap is not updated now

    def pop(self):
        ans = heappop(self.heap)
        # check if the minimum was already deleted
        # basically sync the heap and dictionary where possible
        while self.counter[ans] == 0:
            ans = heappop(self.heap)
        self.counter[ans] -= 1
        return ans

    def min(self):
        # breaks down (intentionally) if the structure is empty
        ans = self.heap[0]  # the current min in the heap
        # same sync as in the "pop" method
        while self.counter[ans] == 0:
            heappop(self.heap)  # remove the already deleted min
            ans = self.heap[0]  # consider the new min
        return ans


# we obtain the max heap by putting the opposite in a min heap
# we pretend the actual numbers are in heap but the opposites are
class DeletableMaxHeap:
    def __init__(self):
        self.heap = []
        self.counter = defaultdict(int)

    def __contains__(self, x):
        if (-x in self.counter) and (self.counter[-x] > 0):
            return True
        else:
            return False

    def push(self, x):
        heappush(self.heap, -x)
        self.counter[-x] += 1

    def delete(self, x):
        # it breaks down (intentioanlly) if x not in the structure
        assert self.counter[-x] > 0
        self.counter[-x] -= 1
        # note that the heap is not updated now

    def pop(self):
        ans = heappop(self.heap)
        # check if the maximum was already deleted
        # basically sync the heap and dictionary where possible
        while self.counter[ans] == 0:
            ans = heappop(self.heap)
        self.counter[ans] -= 1
        return -ans

    def max(self):
        # breaks down (intentionally) if the structure is empty
        ans = self.heap[0]  # the current min in the heap
        # same sync as in the "pop" method
        while self.counter[ans] == 0:
            heappop(self.heap)  # remove the already deleted min
            ans = self.heap[0]  # consider the new min
        return -ans
