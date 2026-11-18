"""
Python cheat sheet for coding problems / interviews.

Every section is a function full of runnable snippets with asserts, so the
whole file doubles as a self-check:

    python3 cheatsheet.py            # run every section
    python3 cheatsheet.py heaps      # run sections whose name contains "heaps"

Sections
  1. Core data structures      list, tuple, str, dict, set
  2. collections               Counter, defaultdict, deque, OrderedDict, namedtuple
  3. heapq & bisect            priority queues, binary search
  4. Sorting                   key functions, stability, custom comparators
  5. Functional constructs     comprehensions, generators, lambda, map/filter/reduce,
                               itertools, functools, closures, decorators
  6. Classes                   dataclass, dunders, properties, class/static methods,
                               inheritance, ABC, Enum, context managers, __slots__
  7. Threads                   Thread, Lock, Queue, Event, Semaphore, executors, GIL
  8. asyncio                   coroutines, gather, tasks, TaskGroup, timeouts,
                               Queue, Semaphore, to_thread, async generators
  9. Algorithm templates       binary search, BFS, DFS, union-find, backtracking, DP,
                               sliding window, monotonic stack, linked list, trees
 10. Gotchas                   the mistakes that cost points

BIG-O CHEAT TABLE (average case)
  list    : index O(1), append/pop() O(1), insert/pop(0)/remove O(n), `in` O(n),
            slice O(k), sort O(n log n)
  dict/set: get/set/del/`in` O(1)
  deque   : append/appendleft/pop/popleft O(1), index in the middle O(n)
  heapq   : push/pop O(log n), heapify O(n), peek h[0] O(1)
  bisect  : search O(log n), insort O(n) (because of the list shift)
  str     : concatenation in a loop is O(n^2): build a list and ''.join() it
"""

from __future__ import annotations

import asyncio
import bisect
import functools
import heapq
import itertools
import operator
import queue
import sys
import threading
import time
from abc import ABC, abstractmethod
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import NamedTuple


# =============================================================================
# 1. CORE DATA STRUCTURES
# =============================================================================
def core_data_structures():
    # ---- list: dynamic array -------------------------------------------------
    a = [3, 1, 2]
    a.append(4)                 # [3, 1, 2, 4]
    a.extend([5, 6])            # [3, 1, 2, 4, 5, 6]
    a.insert(0, 0)              # O(n): shifts everything
    assert a.pop() == 6         # O(1) from the end (use as a STACK)
    assert a.pop(0) == 0        # O(n) from the front: use deque instead
    a.remove(2)                 # removes first occurrence, O(n), ValueError if missing
    assert a == [3, 1, 4, 5]
    assert a.index(4) == 2
    assert a[-1] == 5 and a[::-1] == [5, 4, 1, 3]   # negative index, reverse copy
    assert a[1:3] == [1, 4]     # slice is a COPY
    b = a[:]                    # shallow copy (also list(a), a.copy())
    b.sort()                    # in place, returns None
    assert sorted(a) == [1, 3, 4, 5] and a == [3, 1, 4, 5]  # sorted() returns new list
    a.reverse()                 # in place

    grid = [[0] * 3 for _ in range(2)]   # 2x3 matrix, correct way
    grid[0][0] = 1
    assert grid == [[1, 0, 0], [0, 0, 0]]
    transposed = [list(col) for col in zip(*grid)]
    assert transposed == [[1, 0], [0, 0], [0, 0]]

    # unpacking
    first, *middle, last = [1, 2, 3, 4]
    assert (first, middle, last) == (1, [2, 3], 4)
    x, y = 1, 2
    x, y = y, x                 # swap
    assert (x, y) == (2, 1)

    # enumerate / zip
    for i, v in enumerate(["a", "b"], start=1):
        pass
    assert list(zip("ab", [1, 2, 3])) == [("a", 1), ("b", 2)]   # stops at shortest
    assert dict(zip("ab", [1, 2])) == {"a": 1, "b": 2}

    # useful builtins
    nums = [4, -1, 7]
    assert (min(nums), max(nums), sum(nums)) == (-1, 7, 10)
    assert max(nums, key=abs) == 7
    assert max([], default=0) == 0
    assert any(n < 0 for n in nums) and not all(n > 0 for n in nums)
    assert divmod(17, 5) == (3, 2)
    assert -7 // 2 == -4 and int(-7 / 2) == -3   # // floors toward -inf!
    assert -7 % 3 == 2                           # result has the sign of the divisor
    INF = float("inf")
    assert min(INF, 5) == 5
    assert abs(-3) == 3 and pow(2, 10, 1000) == 24   # modular pow

    # ---- tuple: immutable, hashable (if contents are) -> dict keys / set items
    t = (1, 2)
    single = (1,)               # trailing comma makes a 1-tuple
    visited = {(0, 0), (0, 1)}  # coordinates in a set
    assert (0, 1) in visited and len(single) == 1
    assert (1, 2) < (1, 3) < (2, 0)   # tuples compare lexicographically

    # ---- str: immutable ------------------------------------------------------
    s = "Hello, World"
    assert s.lower() == "hello, world" and s.upper().isupper()
    assert s.split(", ") == ["Hello", "World"]
    assert "a b  c".split() == ["a", "b", "c"]   # no arg: splits on any whitespace
    assert "-".join(["a", "b"]) == "a-b"
    assert "  x ".strip() == "x"
    assert s.startswith("He") and s.endswith("ld")
    assert s.find("o") == 4 and s.find("z") == -1   # .index() raises instead
    assert s.replace("l", "L", 1) == "HeLlo, World"
    assert s.count("l") == 3
    assert "abc"[::-1] == "cba"
    assert "a1".isalnum() and "12".isdigit() and "ab".isalpha()
    assert ord("a") == 97 and chr(97) == "a"
    assert ord("c") - ord("a") == 2          # letter -> 0..25 index
    assert f"{3.14159:.2f}" == "3.14" and f"{5:03d}" == "005" and f"{255:b}" == "11111111"
    chars = list("abc")
    chars[0] = "z"                           # mutate via list, then join
    assert "".join(chars) == "zbc"
    assert int("101", 2) == 5 and bin(5) == "0b101" and hex(255) == "0xff"

    # ---- dict: hash map, preserves insertion order (3.7+) -------------------
    d = {"a": 1}
    d["b"] = 2
    assert d.get("z") is None and d.get("z", 0) == 0
    d.setdefault("c", []).append(3)          # insert default if missing, return it
    assert d["c"] == [3]
    assert d.pop("c") == [3] and d.pop("zz", None) is None
    for k, v in d.items():
        pass
    assert list(d.keys()) == ["a", "b"] and list(d.values()) == [1, 2]
    merged = d | {"b": 20, "c": 3}            # 3.9+ merge (right wins)
    assert merged == {"a": 1, "b": 20, "c": 3}
    inverted = {v: k for k, v in d.items()}
    assert inverted == {1: "a", 2: "b"}
    assert max(d, key=d.get) == "b"           # key with max value
    # NOTE: don't add/remove keys while iterating; iterate over list(d) instead.

    # ---- set: hash set -------------------------------------------------------
    s1, s2 = {1, 2, 3}, {2, 3, 4}
    assert s1 & s2 == {2, 3}                  # intersection
    assert s1 | s2 == {1, 2, 3, 4}            # union
    assert s1 - s2 == {1}                     # difference
    assert s1 ^ s2 == {1, 4}                  # symmetric difference
    assert {2, 3} <= s1                       # subset
    s1.add(9); s1.discard(100)                # discard: no error if missing
    empty = set()                             # {} is an empty DICT
    frozen = frozenset({1, 2})                # hashable set -> usable as dict key
    assert isinstance(empty, set) and {frozen: "ok"}[frozenset({2, 1})] == "ok"
    assert len(set([1, 1, 2])) == 2           # dedupe (order lost)
    assert list(dict.fromkeys([3, 1, 3, 2])) == [3, 1, 2]   # dedupe, keep order


# =============================================================================
# 2. COLLECTIONS MODULE
# =============================================================================
def collections_module():
    # ---- Counter: multiset / frequency map ----------------------------------
    c = Counter("abracadabra")
    assert c["a"] == 5 and c["z"] == 0        # missing key -> 0, no KeyError
    assert c.most_common(2) == [("a", 5), ("b", 2)]
    assert Counter("listen") == Counter("silent")   # anagram check
    c2 = Counter(a=1, b=5)
    assert (c - c2)["b"] == 0                 # subtraction drops <= 0 counts
    assert (c + c2)["b"] == 7
    assert c2 & Counter(b=2) == Counter(b=2)  # min of counts
    c.update("aaa"); c.subtract("a")
    assert c["a"] == 7
    assert c.total() == 13                    # 3.10+

    # ---- defaultdict: auto-create missing values -----------------------------
    graph = defaultdict(list)
    for u, v in [(1, 2), (1, 3), (2, 3)]:
        graph[u].append(v)
        graph[v].append(u)                    # undirected
    assert graph[1] == [2, 3]

    groups = defaultdict(list)                # group anagrams
    for w in ["eat", "tea", "tan", "nat"]:
        groups["".join(sorted(w))].append(w)
    assert sorted(groups.values()) == [["eat", "tea"], ["tan", "nat"]]

    counts = defaultdict(int)
    counts["x"] += 1
    nested = defaultdict(lambda: defaultdict(int))   # 2-level auto-dict
    nested["a"]["b"] += 1
    assert nested["a"]["b"] == 1
    # careful: merely READING graph[99] inserts an empty list. Use `99 in graph`.

    # ---- deque: double-ended queue -------------------------------------------
    q = deque([1, 2, 3])
    q.append(4); q.appendleft(0)
    assert q.popleft() == 0 and q.pop() == 4
    assert q[0] == 1 and q[-1] == 3           # peek both ends
    q.rotate(1)                               # [3, 1, 2]
    assert list(q) == [3, 1, 2]
    window = deque(maxlen=3)                  # fixed-size: old items fall off
    for i in range(5):
        window.append(i)
    assert list(window) == [2, 3, 4]

    # ---- OrderedDict: LRU cache building block -------------------------------
    class LRUCache:
        def __init__(self, capacity: int):
            self.cap = capacity
            self.data: OrderedDict[int, int] = OrderedDict()

        def get(self, key: int) -> int:
            if key not in self.data:
                return -1
            self.data.move_to_end(key)        # mark as most recently used
            return self.data[key]

        def put(self, key: int, value: int) -> None:
            self.data[key] = value
            self.data.move_to_end(key)
            if len(self.data) > self.cap:
                self.data.popitem(last=False) # evict least recently used

    lru = LRUCache(2)
    lru.put(1, 1); lru.put(2, 2); lru.get(1); lru.put(3, 3)
    assert lru.get(2) == -1 and lru.get(1) == 1

    # ---- namedtuple: lightweight immutable record ----------------------------
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    assert p.x == 1 and p == (1, 2)
    assert p._replace(x=5) == Point(5, 2)


# =============================================================================
# 3. HEAPQ & BISECT
# =============================================================================
def heaps_and_bisect():
    # ---- heapq: MIN-heap on a plain list -------------------------------------
    h = []
    for x in [5, 1, 8, 3]:
        heapq.heappush(h, x)
    assert h[0] == 1                          # peek smallest
    assert heapq.heappop(h) == 1

    nums = [5, 1, 8, 3, 9]
    heapq.heapify(nums)                       # O(n), in place
    assert heapq.nsmallest(2, [5, 1, 8]) == [1, 5]
    assert heapq.nlargest(2, [5, 1, 8]) == [8, 5]

    # MAX-heap: push negatives
    mh = []
    for x in [5, 1, 8]:
        heapq.heappush(mh, -x)
    assert -heapq.heappop(mh) == 8

    # tuples: ordered by first element, ties broken by the next.
    # Add a counter so non-comparable payloads (dicts, objects) never get compared.
    tasks = []
    counter = itertools.count()
    heapq.heappush(tasks, (2, next(counter), {"name": "b"}))
    heapq.heappush(tasks, (1, next(counter), {"name": "a"}))
    assert heapq.heappop(tasks)[2]["name"] == "a"

    # top-k frequent with a size-k heap: O(n log k)
    words = ["a", "b", "a", "c", "b", "a"]
    k_heap = []
    for w, cnt in Counter(words).items():
        heapq.heappush(k_heap, (cnt, w))
        if len(k_heap) > 2:
            heapq.heappop(k_heap)             # drop the smallest
    assert sorted(k_heap, reverse=True) == [(3, "a"), (2, "b")]

    # merge k sorted iterables
    assert list(heapq.merge([1, 4], [2, 5], [3])) == [1, 2, 3, 4, 5]
    # heappushpop / heapreplace: push+pop in one step (faster)
    h = [1, 3, 5]
    assert heapq.heappushpop(h, 0) == 0       # push then pop
    assert heapq.heapreplace(h, 4) == 1       # pop then push

    # ---- bisect: binary search on a SORTED list ------------------------------
    arr = [1, 2, 4, 4, 4, 7]
    assert bisect.bisect_left(arr, 4) == 2    # first index where arr[i] >= x
    assert bisect.bisect_right(arr, 4) == 5   # first index where arr[i] > x
    assert bisect.bisect_right(arr, 4) - bisect.bisect_left(arr, 4) == 3  # count of 4
    i = bisect.bisect_left(arr, 5)
    assert i < len(arr) and arr[i] == 7       # "ceiling" of 5
    bisect.insort(arr, 3)                     # keeps arr sorted
    assert arr == [1, 2, 3, 4, 4, 4, 7]
    # key= (3.10+): search a list of records by a field
    people = [("ann", 20), ("bob", 30), ("cat", 40)]
    assert bisect.bisect_left(people, 30, key=lambda p: p[1]) == 1


# =============================================================================
# 4. SORTING
# =============================================================================
def sorting():
    words = ["banana", "Apple", "cherry", "fig"]
    assert sorted(words, key=str.lower) == ["Apple", "banana", "cherry", "fig"]
    assert sorted(words, key=len) == ["fig", "Apple", "banana", "cherry"]  # stable!
    assert sorted(words, key=len, reverse=True)[0] in ("banana", "cherry")

    # multi-key: by length desc, then alphabetically asc -> negate numeric keys
    assert sorted(words, key=lambda w: (-len(w), w)) == ["banana", "cherry", "Apple", "fig"]

    intervals = [[5, 6], [1, 3], [2, 4]]
    intervals.sort(key=lambda iv: iv[0])
    assert intervals == [[1, 3], [2, 4], [5, 6]]

    recs = [{"n": "b", "a": 2}, {"n": "a", "a": 2}, {"n": "c", "a": 1}]
    assert [r["n"] for r in sorted(recs, key=operator.itemgetter("a", "n"))] == ["c", "a", "b"]

    # custom comparator (when a key is awkward): "largest number" problem
    def cmp(x: str, y: str) -> int:
        return -1 if x + y > y + x else (1 if x + y < y + x else 0)
    assert "".join(sorted(["3", "30", "34", "5", "9"], key=functools.cmp_to_key(cmp))) == "9534330"

    # argsort: indices that would sort the list
    vals = [30, 10, 20]
    assert sorted(range(len(vals)), key=vals.__getitem__) == [1, 2, 0]


# =============================================================================
# 5. FUNCTIONAL CONSTRUCTS
# =============================================================================
def functional():
    # ---- comprehensions ------------------------------------------------------
    sq = [x * x for x in range(5) if x % 2 == 0]           # list
    assert sq == [0, 4, 16]
    assert {x % 3 for x in range(10)} == {0, 1, 2}         # set
    assert {c: ord(c) for c in "ab"} == {"a": 97, "b": 98} # dict
    flat = [x for row in [[1, 2], [3]] for x in row]       # nested: outer loop first
    assert flat == [1, 2, 3]
    labels = ["even" if x % 2 == 0 else "odd" for x in range(3)]   # if/else goes BEFORE for
    assert labels == ["even", "odd", "even"]

    # ---- generators: lazy, single-pass, O(1) memory --------------------------
    gen = (x * x for x in range(10**9))     # nothing computed yet
    assert next(gen) == 0 and next(gen) == 1
    assert sum(x for x in range(5)) == 10   # parentheses optional as only argument

    def fib():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    assert list(itertools.islice(fib(), 6)) == [0, 1, 1, 2, 3, 5]

    def flatten(xs):
        for x in xs:
            if isinstance(x, list):
                yield from flatten(x)       # delegate to a sub-generator
            else:
                yield x
    assert list(flatten([1, [2, [3, 4]], 5])) == [1, 2, 3, 4, 5]

    # ---- lambda, map, filter, reduce -----------------------------------------
    add = lambda a, b: a + b                # noqa: E731 (fine for one-liners / keys)
    assert add(1, 2) == 3
    assert list(map(int, "1 2 3".split())) == [1, 2, 3]
    assert list(map(operator.add, [1, 2], [10, 20])) == [11, 22]
    assert list(filter(None, [0, 1, "", "a"])) == [1, "a"]  # None: keep truthy
    assert functools.reduce(operator.mul, [1, 2, 3, 4], 1) == 24
    assert functools.reduce(lambda acc, x: acc ^ x, [4, 1, 4]) == 1   # find the single number

    # ---- itertools -----------------------------------------------------------
    it = itertools
    assert list(it.accumulate([1, 2, 3])) == [1, 3, 6]                 # prefix sums
    assert list(it.accumulate([1, 2, 3], initial=0)) == [0, 1, 3, 6]
    assert list(it.accumulate([3, 1, 5], max)) == [3, 3, 5]            # running max
    assert list(it.combinations("abc", 2)) == [("a", "b"), ("a", "c"), ("b", "c")]
    assert len(list(it.permutations("abc"))) == 6
    assert list(it.product([0, 1], repeat=2)) == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert list(it.combinations_with_replacement("ab", 2)) == [("a", "a"), ("a", "b"), ("b", "b")]
    assert list(it.chain([1], [2, 3])) == [1, 2, 3]
    assert list(it.chain.from_iterable([[1], [2]])) == [1, 2]
    assert [(k, len(list(g))) for k, g in it.groupby("aaabcc")] == [("a", 3), ("b", 1), ("c", 2)]  # run-length
    assert list(it.pairwise([1, 2, 4])) == [(1, 2), (2, 4)]           # 3.10+
    assert list(it.zip_longest("ab", "x", fillvalue="-")) == [("a", "x"), ("b", "-")]
    assert list(it.islice(it.count(10, 5), 3)) == [10, 15, 20]
    assert list(it.repeat(7, 2)) == [7, 7]
    assert list(it.takewhile(lambda x: x < 3, [1, 2, 5, 1])) == [1, 2]
    assert list(it.dropwhile(lambda x: x < 3, [1, 2, 5, 1])) == [5, 1]
    assert list(it.starmap(pow, [(2, 3), (3, 2)])) == [8, 9]
    assert list(it.batched(range(5), 2)) == [(0, 1), (2, 3), (4,)]     # 3.12+

    # ---- functools -----------------------------------------------------------
    @functools.cache                        # unbounded memo (lru_cache(maxsize=None))
    def ways(n: int) -> int:                # args must be hashable
        return 1 if n <= 1 else ways(n - 1) + ways(n - 2)
    assert ways(80) == 37889062373143906
    ways.cache_clear()

    @functools.lru_cache(maxsize=128)       # bounded memo
    def slow_square(x):
        return x * x
    slow_square(3); slow_square(3)
    assert slow_square.cache_info().hits == 1

    base2 = functools.partial(int, base=2)  # pre-fill arguments
    assert base2("110") == 6

    # ---- closures ------------------------------------------------------------
    def make_counter():
        count = 0
        def inc():
            nonlocal count                  # needed to REBIND an outer variable
            count += 1
            return count
        return inc
    c = make_counter()
    c(); assert c() == 2

    # late-binding gotcha: lambdas capture the variable, not its value
    fs = [lambda: i for i in range(3)]
    assert [f() for f in fs] == [2, 2, 2]
    fs = [lambda i=i: i for i in range(3)]  # fix: bind as default arg
    assert [f() for f in fs] == [0, 1, 2]

    # ---- decorators ----------------------------------------------------------
    def timed(fn):
        @functools.wraps(fn)                # keep fn.__name__/__doc__
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                wrapper.last_elapsed = time.perf_counter() - start
        return wrapper

    def retry(times: int):                  # decorator WITH arguments = 3 levels
        def deco(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                for attempt in range(times):
                    try:
                        return fn(*args, **kwargs)
                    except ValueError:
                        if attempt == times - 1:
                            raise
            return wrapper
        return deco

    calls = []
    @timed
    @retry(times=3)                         # applied bottom-up: timed(retry(3)(flaky))
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError
        return "ok"
    assert flaky() == "ok" and len(calls) == 3 and flaky.__name__ == "flaky"
    assert flaky.last_elapsed >= 0

    # ---- *args / **kwargs / keyword-only / positional-only -------------------
    def f(a, b=2, /, *args, c, d=4, **kwargs):   # a,b positional-only; c,d keyword-only
        return a, b, args, c, d, kwargs
    assert f(1, 9, 8, c=3, z=0) == (1, 9, (8,), 3, 4, {"z": 0})
    assert f(*[1, 2], **{"c": 3}) == (1, 2, (), 3, 4, {})

    # ---- walrus operator ------------------------------------------------------
    data = [1, 5, 9]
    if (n := len(data)) > 2:
        assert n == 3

    # ---- match statement (3.10+) ---------------------------------------------
    def describe(cmd):
        match cmd:
            case ["go", direction]:
                return f"move {direction}"
            case {"op": "add", "args": [x, y]}:
                return x + y
            case int() | float() as num if num < 0:
                return "negative"
            case _:
                return "unknown"
    assert describe(["go", "north"]) == "move north"
    assert describe({"op": "add", "args": [1, 2]}) == 3
    assert describe(-1) == "negative" and describe("?") == "unknown"


# =============================================================================
# 6. CLASSES
# =============================================================================
def classes():
    # ---- plain class with the dunders that matter ----------------------------
    class Vector:
        dims = 2                                    # class attribute (shared)

        def __init__(self, x: float, y: float):
            self.x, self.y = x, y                   # instance attributes

        def __repr__(self):                         # for debugging / REPL
            return f"Vector({self.x}, {self.y})"

        def __eq__(self, other):
            return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

        def __hash__(self):                         # needed if you define __eq__
            return hash((self.x, self.y))           # and want set/dict keys

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __lt__(self, other):                    # enables sorted() and heapq
            return (self.x, self.y) < (other.x, other.y)

        def __len__(self):
            return 2

        def __iter__(self):                         # enables unpacking: x, y = v
            yield self.x
            yield self.y

        def __getitem__(self, i):
            return (self.x, self.y)[i]

        def __bool__(self):
            return bool(self.x or self.y)

    v = Vector(1, 2) + Vector(3, 4)
    assert v == Vector(4, 6) and repr(v) == "Vector(4, 6)"
    assert {Vector(1, 1), Vector(1, 1)} == {Vector(1, 1)}
    assert sorted([Vector(2, 0), Vector(1, 5)])[0] == Vector(1, 5)
    x, y = v
    assert (x, y, v[0], len(v), bool(Vector(0, 0))) == (4, 6, 4, 2, False)

    # ---- dataclass: generates __init__, __repr__, __eq__ ---------------------
    @dataclass(order=True)                          # order=True -> <, <= etc. by fields
    class Task:
        priority: int
        name: str = field(compare=False)            # excluded from comparisons
        tags: list[str] = field(default_factory=list, compare=False)  # never `= []`

    t1, t2 = Task(2, "write"), Task(1, "read")
    assert sorted([t1, t2])[0].name == "read"       # works with heapq too
    t1.tags.append("x")
    assert Task(3, "a").tags == []                  # not shared

    @dataclass(frozen=True)                         # immutable + hashable
    class Coord:
        r: int
        c: int
    assert Coord(0, 1) in {Coord(0, 1)}

    @dataclass(slots=True)                          # 3.10+: less memory, faster attrs
    class Node:
        val: int
        next: "Node | None" = None
    head = Node(1, Node(2))
    assert head.next.val == 2

    # ---- typing.NamedTuple: typed immutable record ---------------------------
    class Edge(NamedTuple):
        u: int
        v: int
        w: float = 1.0
    assert Edge(1, 2).w == 1.0 and Edge(1, 2, 3)[2] == 3

    # ---- properties, classmethod, staticmethod -------------------------------
    class Temperature:
        def __init__(self, celsius: float):
            self._c = celsius                       # leading _ = "private" by convention

        @property
        def fahrenheit(self) -> float:              # computed attribute
            return self._c * 9 / 5 + 32

        @property
        def celsius(self):
            return self._c

        @celsius.setter
        def celsius(self, value):                   # validation on assignment
            if value < -273.15:
                raise ValueError("below absolute zero")
            self._c = value

        @classmethod
        def from_fahrenheit(cls, f: float):         # alternative constructor
            return cls((f - 32) * 5 / 9)

        @staticmethod
        def is_freezing(c: float) -> bool:          # no self/cls: just namespaced
            return c <= 0

    t = Temperature.from_fahrenheit(212)
    assert t.celsius == 100 and t.fahrenheit == 212
    t.celsius = 0
    assert Temperature.is_freezing(t.celsius)
    try:
        t.celsius = -300
        raise AssertionError("should have raised")
    except ValueError:
        pass

    # ---- inheritance, super(), abstract base classes -------------------------
    class Shape(ABC):
        def __init__(self, name):
            self.name = name

        @abstractmethod
        def area(self) -> float: ...

        def describe(self):                          # template method
            return f"{self.name}: {self.area():.1f}"

    class Rect(Shape):
        def __init__(self, w, h):
            super().__init__("rect")
            self.w, self.h = w, h

        def area(self):
            return self.w * self.h

    class Square(Rect):
        def __init__(self, s):
            super().__init__(s, s)
            self.name = "square"

    assert Square(3).describe() == "square: 9.0"
    assert isinstance(Square(1), Shape) and issubclass(Square, Rect)
    assert [c.__name__ for c in Square.__mro__][:3] == ["Square", "Rect", "Shape"]
    try:
        Shape("x")                                   # can't instantiate abstract
        raise AssertionError
    except TypeError:
        pass

    # ---- Enum ----------------------------------------------------------------
    class Color(Enum):
        RED = auto()
        GREEN = auto()
    assert Color.RED.name == "RED" and Color["GREEN"] is Color.GREEN
    assert [c.name for c in Color] == ["RED", "GREEN"]

    # ---- context managers ----------------------------------------------------
    log = []

    class Managed:
        def __enter__(self):
            log.append("enter")
            return self
        def __exit__(self, exc_type, exc, tb):
            log.append("exit")
            return False                             # True would swallow the exception

    @contextmanager                                  # generator-based shortcut
    def managed():
        log.append("open")
        try:
            yield "resource"
        finally:
            log.append("close")

    with Managed(), managed() as r:
        assert r == "resource"
    assert log == ["enter", "open", "close", "exit"]

    # ---- __slots__, __call__, class-level registry ---------------------------
    class Point:
        __slots__ = ("x", "y")                       # no __dict__: saves memory
        def __init__(self, x, y):
            self.x, self.y = x, y
    try:
        Point(1, 2).z = 3
        raise AssertionError
    except AttributeError:
        pass

    class Adder:
        def __init__(self, n): self.n = n
        def __call__(self, x): return x + self.n     # instance usable as a function
    assert Adder(5)(1) == 6

    # ---- linked-list / tree nodes as typically given in problems -------------
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val, self.next = val, next

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val, self.left, self.right = val, left, right

    def reverse(head):
        prev = None
        while head:
            head.next, prev, head = prev, head, head.next
        return prev
    r = reverse(ListNode(1, ListNode(2, ListNode(3))))
    assert [r.val, r.next.val, r.next.next.val] == [3, 2, 1]

    def max_depth(node):
        return 0 if not node else 1 + max(max_depth(node.left), max_depth(node.right))
    assert max_depth(TreeNode(1, TreeNode(2, TreeNode(3)), TreeNode(4))) == 3


# =============================================================================
# 7. THREADS
# =============================================================================
def threads():
    """
    GIL: only one thread runs Python bytecode at a time (in standard CPython).
      - Threads speed up I/O-bound work (network, disk, sleep): the GIL is released while waiting.
      - CPU-bound work -> multiprocessing / ProcessPoolExecutor (or the free-threaded 3.13t build).
    Even with the GIL, `x += 1` is NOT atomic -> protect shared state with a Lock.
    """
    # ---- Thread + Lock ---------------------------------------------------------
    counter = 0
    lock = threading.Lock()

    def work(n):
        nonlocal counter
        for _ in range(n):
            with lock:                       # acquire/release automatically
                counter += 1

    ts = [threading.Thread(target=work, args=(10_000,)) for _ in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()                             # wait for completion
    assert counter == 40_000
    # RLock: same thread may re-acquire (recursive code). daemon=True: don't block exit.

    # ---- producer / consumer with queue.Queue (thread-safe) -------------------
    q: queue.Queue[int | None] = queue.Queue(maxsize=10)
    results = []
    SENTINEL = None

    def producer():
        for i in range(5):
            q.put(i)                         # blocks if full
        q.put(SENTINEL)

    def consumer():
        while (item := q.get()) is not SENTINEL:   # blocks if empty
            results.append(item * 10)
            q.task_done()
        q.task_done()

    p, c = threading.Thread(target=producer), threading.Thread(target=consumer)
    p.start(); c.start(); p.join(); c.join()
    assert results == [0, 10, 20, 30, 40]

    # ---- Event: one-shot signal between threads -------------------------------
    ready = threading.Event()
    seen = []
    waiter = threading.Thread(target=lambda: (ready.wait(timeout=2), seen.append("go")))
    waiter.start()
    ready.set()
    waiter.join()
    assert seen == ["go"]

    # ---- Semaphore: cap concurrency -------------------------------------------
    sem = threading.Semaphore(2)
    active, peak = 0, 0
    peak_lock = threading.Lock()

    def limited():
        nonlocal active, peak
        with sem:
            with peak_lock:
                active += 1
                peak = max(peak, active)
            time.sleep(0.01)
            with peak_lock:
                active -= 1

    ts = [threading.Thread(target=limited) for _ in range(6)]
    for t in ts: t.start()
    for t in ts: t.join()
    assert peak <= 2

    # ---- Condition: wait until a predicate holds ------------------------------
    cond = threading.Condition()
    items: list[int] = []

    def wait_for_item():
        with cond:
            cond.wait_for(lambda: len(items) > 0, timeout=2)
            seen.append(items[0])

    w = threading.Thread(target=wait_for_item)
    w.start()
    with cond:
        items.append(42)
        cond.notify_all()
    w.join()
    assert seen[-1] == 42

    # ---- ThreadPoolExecutor: the usual high-level choice ----------------------
    def fetch(x):
        time.sleep(0.01)                     # pretend I/O
        return x * x

    with ThreadPoolExecutor(max_workers=4) as pool:
        assert list(pool.map(fetch, range(5))) == [0, 1, 4, 9, 16]   # keeps input order
        futures = {pool.submit(fetch, i): i for i in range(3)}
        done = {futures[f]: f.result() for f in as_completed(futures)}  # completion order
    assert done == {0: 0, 1: 1, 2: 4}
    # ProcessPoolExecutor has the same API for CPU-bound work
    # (the function must be defined at module top level so it can be pickled).

    # ---- thread-local data -----------------------------------------------------
    local = threading.local()
    local.name = "main"
    out = []
    t = threading.Thread(target=lambda: out.append(getattr(local, "name", "unset")))
    t.start(); t.join()
    assert out == ["unset"]                  # each thread sees its own attributes


# =============================================================================
# 8. ASYNCIO
# =============================================================================
def asyncio_section():
    """
    Single thread, cooperative multitasking: code yields control only at `await`.
    Great for many concurrent I/O tasks. Never call blocking code (time.sleep,
    requests.get) inside a coroutine; use asyncio.sleep or asyncio.to_thread.
    """

    async def fetch(i: int, delay: float = 0.01) -> int:
        await asyncio.sleep(delay)          # yields to the event loop
        return i * 10

    async def main():
        # ---- sequential vs concurrent ----------------------------------------
        r = await fetch(1)                  # calling fetch() alone only creates a coroutine
        assert r == 10

        results = await asyncio.gather(*(fetch(i) for i in range(5)))   # concurrent
        assert results == [0, 10, 20, 30, 40]                           # input order

        # return_exceptions=True: one failure doesn't cancel/raise for the rest
        async def boom():
            raise ValueError("bad")
        res = await asyncio.gather(fetch(1), boom(), return_exceptions=True)
        assert res[0] == 10 and isinstance(res[1], ValueError)

        # ---- tasks: start now, await later -----------------------------------
        task = asyncio.create_task(fetch(7))   # keep a reference so it isn't GC'd
        # ... do other work here ...
        assert await task == 70

        # ---- TaskGroup (3.11+): structured concurrency -----------------------
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(fetch(1))
            t2 = tg.create_task(fetch(2))
        assert (t1.result(), t2.result()) == (10, 20)   # all done when the block exits
        # if one task fails, the others are cancelled and an ExceptionGroup is raised:
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(boom())
                tg.create_task(fetch(1, delay=1))
        except* ValueError as eg:
            assert len(eg.exceptions) == 1

        # ---- timeouts ------------------------------------------------------------
        try:
            await asyncio.wait_for(fetch(1, delay=1), timeout=0.01)
            raise AssertionError
        except TimeoutError:                # asyncio.TimeoutError is TimeoutError in 3.11+
            pass
        try:
            async with asyncio.timeout(0.01):   # 3.11+ context manager form
                await asyncio.sleep(1)
        except TimeoutError:
            pass

        # ---- as_completed: handle results as they finish ---------------------
        order = []
        for coro in asyncio.as_completed([fetch(1, 0.03), fetch(2, 0.01)]):
            order.append(await coro)
        assert order == [20, 10]

        # ---- Semaphore: limit concurrency (e.g. max N open requests) ---------
        sem = asyncio.Semaphore(2)
        active = peak = 0
        async def limited(i):
            nonlocal active, peak
            async with sem:
                active += 1
                peak = max(peak, active)
                await asyncio.sleep(0.01)
                active -= 1
        await asyncio.gather(*(limited(i) for i in range(6)))
        assert peak == 2

        # ---- Lock: no data races between awaits, but logical races still exist
        lock = asyncio.Lock()
        balance = 0
        async def deposit():
            nonlocal balance
            async with lock:
                cur = balance
                await asyncio.sleep(0)      # without the lock, updates would be lost here
                balance = cur + 1
        await asyncio.gather(*(deposit() for _ in range(10)))
        assert balance == 10

        # ---- Queue: producer / consumer with worker pool ---------------------
        q: asyncio.Queue[int] = asyncio.Queue()
        out = []
        async def worker():
            while True:
                item = await q.get()
                out.append(item * 2)
                q.task_done()
        workers = [asyncio.create_task(worker()) for _ in range(3)]
        for i in range(5):
            q.put_nowait(i)
        await q.join()                      # wait until every item is task_done()
        for w in workers:
            w.cancel()                      # stop the infinite loops
        await asyncio.gather(*workers, return_exceptions=True)
        assert sorted(out) == [0, 2, 4, 6, 8]

        # ---- Event -----------------------------------------------------------
        ev = asyncio.Event()
        async def waiter():
            await ev.wait()
            return "released"
        wt = asyncio.create_task(waiter())
        await asyncio.sleep(0)
        ev.set()
        assert await wt == "released"

        # ---- running blocking code without freezing the loop ----------------
        def blocking_io(x):
            time.sleep(0.01)
            return x + 1
        assert await asyncio.to_thread(blocking_io, 1) == 2

        # ---- async generators & async comprehensions ------------------------
        async def ticker(n):
            for i in range(n):
                await asyncio.sleep(0)
                yield i
        assert [i async for i in ticker(3)] == [0, 1, 2]

        # ---- async context manager -------------------------------------------
        class Conn:
            async def __aenter__(self):
                await asyncio.sleep(0)
                return self
            async def __aexit__(self, *exc):
                await asyncio.sleep(0)
                return False
        async with Conn() as conn:
            assert isinstance(conn, Conn)

        # ---- cancellation ----------------------------------------------------
        async def long_job():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                # cleanup here, then re-raise
                raise
        lj = asyncio.create_task(long_job())
        await asyncio.sleep(0)
        lj.cancel()
        try:
            await lj
        except asyncio.CancelledError:
            pass
        assert lj.cancelled()

    asyncio.run(main())                     # entry point: creates & closes the loop


# =============================================================================
# 9. ALGORITHM TEMPLATES
# =============================================================================
def algorithm_templates():
    # ---- binary search on the answer: first index where predicate is True ----
    def first_true(lo: int, hi: int, pred) -> int:
        while lo < hi:
            mid = (lo + hi) // 2
            if pred(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
    assert first_true(0, 100, lambda x: x * x >= 50) == 8

    # ---- two pointers (sorted array, pair with target sum) --------------------
    def two_sum_sorted(a, target):
        i, j = 0, len(a) - 1
        while i < j:
            s = a[i] + a[j]
            if s == target:
                return i, j
            i, j = (i + 1, j) if s < target else (i, j - 1)
        return None
    assert two_sum_sorted([1, 3, 4, 6, 9], 10) == (0, 4)

    # ---- hash map one-pass (unsorted two sum) ---------------------------------
    def two_sum(nums, target):
        seen = {}
        for i, n in enumerate(nums):
            if target - n in seen:
                return seen[target - n], i
            seen[n] = i
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)

    # ---- sliding window (longest substring without repeats) ------------------
    def longest_unique(s):
        last, left, best = {}, 0, 0
        for right, ch in enumerate(s):
            if last.get(ch, -1) >= left:
                left = last[ch] + 1
            last[ch] = right
            best = max(best, right - left + 1)
        return best
    assert longest_unique("abcabcbb") == 3

    # ---- prefix sums (subarray sum equals k) ----------------------------------
    def subarray_sum(nums, k):
        count, total, seen = 0, 0, Counter({0: 1})
        for n in nums:
            total += n
            count += seen[total - k]
            seen[total] += 1
        return count
    assert subarray_sum([1, 1, 1], 2) == 2

    # ---- monotonic stack (next greater element) -------------------------------
    def next_greater(nums):
        res, stack = [-1] * len(nums), []     # stack of indices, values decreasing
        for i, n in enumerate(nums):
            while stack and nums[stack[-1]] < n:
                res[stack.pop()] = n
            stack.append(i)
        return res
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]

    # ---- BFS on a grid (shortest path, unweighted) ----------------------------
    def shortest_path(grid, start, goal):
        R, C = len(grid), len(grid[0])
        q, seen = deque([(start, 0)]), {start}
        while q:
            (r, c), d = q.popleft()
            if (r, c) == goal:
                return d
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))        # mark when ENQUEUED, not when popped
                    q.append(((nr, nc), d + 1))
        return -1
    g = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
    assert shortest_path(g, (0, 0), (2, 0)) == 6

    # ---- DFS (iterative) + counting components --------------------------------
    def count_islands(grid):
        R, C, seen, n = len(grid), len(grid[0]), set(), 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == "1" and (r, c) not in seen:
                    n += 1
                    stack = [(r, c)]
                    seen.add((r, c))
                    while stack:
                        cr, cc = stack.pop()
                        for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1" and (nr, nc) not in seen:
                                seen.add((nr, nc))
                                stack.append((nr, nc))
        return n
    assert count_islands(["110", "010", "001"]) == 2

    # ---- topological sort (Kahn) / cycle detection ---------------------------
    def topo_order(n, edges):
        adj, indeg = defaultdict(list), [0] * n
        for u, v in edges:
            adj[u].append(v)
            indeg[v] += 1
        q = deque(i for i in range(n) if indeg[i] == 0)
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == n else []   # [] -> cycle
    assert topo_order(4, [(0, 1), (1, 2), (0, 3)]) == [0, 1, 3, 2]
    assert topo_order(2, [(0, 1), (1, 0)]) == []

    # ---- Dijkstra -------------------------------------------------------------
    def dijkstra(adj, src):
        dist = {src: 0}
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float("inf")):
                continue                              # stale entry
            for v, w in adj.get(u, []):
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist
    assert dijkstra({"a": [("b", 1), ("c", 4)], "b": [("c", 2)]}, "a") == {"a": 0, "b": 1, "c": 3}

    # ---- union-find (disjoint set) --------------------------------------------
    class DSU:
        def __init__(self, n):
            self.parent, self.size = list(range(n)), [1] * n
        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]   # path halving
                x = self.parent[x]
            return x
        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return False
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            return True
    dsu = DSU(5)
    dsu.union(0, 1); dsu.union(3, 4)
    assert len({dsu.find(i) for i in range(5)}) == 3

    # ---- backtracking (subsets / permutations) --------------------------------
    def subsets(nums):
        res, path = [], []
        def bt(start):
            res.append(path[:])               # copy!
            for i in range(start, len(nums)):
                path.append(nums[i])
                bt(i + 1)
                path.pop()                    # undo
        bt(0)
        return res
    assert len(subsets([1, 2, 3])) == 8

    def permutations(nums):
        res = []
        def bt(path, remaining):
            if not remaining:
                res.append(path)
                return
            for i in range(len(remaining)):
                bt(path + [remaining[i]], remaining[:i] + remaining[i + 1:])
        bt([], nums)
        return res
    assert len(permutations([1, 2, 3])) == 6

    # ---- dynamic programming: top-down and bottom-up --------------------------
    def coin_change(coins, amount):           # bottom-up, 1-D table
        dp = [0] + [float("inf")] * amount
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a:
                    dp[a] = min(dp[a], dp[a - c] + 1)
        return dp[amount] if dp[amount] != float("inf") else -1
    assert coin_change([1, 2, 5], 11) == 3

    def lcs(a, b):                            # top-down with @cache, 2-D state
        @functools.cache
        def go(i, j):
            if i == len(a) or j == len(b):
                return 0
            if a[i] == b[j]:
                return 1 + go(i + 1, j + 1)
            return max(go(i + 1, j), go(i, j + 1))
        return go(0, 0)
    assert lcs("abcde", "ace") == 3

    def lis(nums):                            # O(n log n) with bisect
        tails = []
        for n in nums:
            i = bisect.bisect_left(tails, n)
            if i == len(tails):
                tails.append(n)
            else:
                tails[i] = n
        return len(tails)
    assert lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    # ---- intervals: merge ------------------------------------------------------
    def merge(intervals):
        out = []
        for s, e in sorted(intervals):
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out
    assert merge([[1, 3], [8, 10], [2, 6]]) == [[1, 6], [8, 10]]

    # ---- bit manipulation ----------------------------------------------------
    n = 0b1011
    assert n & 1 == 1                         # odd?
    assert n.bit_count() == 3                 # popcount (3.10+)
    assert n & (n - 1) == 0b1010              # drop lowest set bit
    assert n & -n == 1                        # isolate lowest set bit
    assert (8 & 7) == 0                       # power of two test: x & (x-1) == 0
    assert 1 << 4 == 16 and (n >> 1) == 0b101
    mask_subsets = [[i for i in range(3) if m >> i & 1] for m in range(1 << 3)]
    assert len(mask_subsets) == 8


# =============================================================================
# 10. GOTCHAS
# =============================================================================
def gotchas():
    # 1. aliased rows
    bad = [[0] * 2] * 2
    bad[0][0] = 1
    assert bad == [[1, 0], [1, 0]]            # both rows changed!

    # 2. mutable default argument is created ONCE
    def append_bad(x, acc=[]):
        acc.append(x)
        return acc
    append_bad(1)
    assert append_bad(2) == [1, 2]
    def append_ok(x, acc=None):
        acc = [] if acc is None else acc
        acc.append(x)
        return acc
    assert append_ok(2) == [2]

    # 3. shallow vs deep copy
    import copy
    orig = [[1], [2]]
    sh, dp = orig[:], copy.deepcopy(orig)
    orig[0].append(9)
    assert sh[0] == [1, 9] and dp[0] == [1]

    # 4. `is` vs `==`: use `is` only for None / sentinels
    assert [1] == [1] and [1] is not [1]

    # 5. recursion limit (~1000 by default): raise it or go iterative
    assert sys.getrecursionlimit() >= 1000
    # sys.setrecursionlimit(10**6)   # deep DFS on 10^5 nodes

    # 6. integer division and rounding
    assert round(2.5) == 2 and round(3.5) == 4    # banker's rounding
    assert 7 // 2 == 3 and -7 // 2 == -4
    assert 0.1 + 0.2 != 0.3                       # use math.isclose
    import math
    assert math.isclose(0.1 + 0.2, 0.3)
    assert math.ceil(7 / 2) == 4 and -(-7 // 2) == 4   # integer ceil without floats

    # 7. modifying a list while iterating it: iterate over a copy or build a new one
    nums = [1, 2, 3, 4]
    nums = [n for n in nums if n % 2]
    assert nums == [1, 3]

    # 8. big integers are unbounded (no overflow); use % (10**9 + 7) when asked
    assert 2 ** 100 > 10 ** 30

    # 9. sort() returns None
    xs = [3, 1]
    assert xs.sort() is None and xs == [1, 3]

    # 10. fast input for big inputs
    # data = sys.stdin.buffer.read().split()   # then map(int, data)


# =============================================================================
SECTIONS = [
    core_data_structures,
    collections_module,
    heaps_and_bisect,
    sorting,
    functional,
    classes,
    threads,
    asyncio_section,
    algorithm_templates,
    gotchas,
]

if __name__ == "__main__":
    wanted = sys.argv[1:]
    for fn in SECTIONS:
        if wanted and not any(w in fn.__name__ for w in wanted):
            continue
        start = time.perf_counter()
        fn()
        print(f"ok  {fn.__name__:<22} {time.perf_counter() - start:6.3f}s")
