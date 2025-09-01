from bisect import bisect_left
from collections import defaultdict, deque
from typing import List, Counter
import heapq


def firstMissingPositive(self, nums: List[int]) -> int:
    n = len(nums)
    i = 0
    while i < n:
        x = nums[i]
        if 1 <= x <= n and nums[x - 1] != x:
            nums[i], nums[x - 1] = nums[x - 1], nums[i]  # swap into it's place
        else:
            i += 1

    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def permute(self, nums: List[int]) -> List[List[int]]:
    results = []
    n = len(nums)

    def backtrack(path, used):
        if len(path) == n:
            results.append(path[:])
            return

        for i, letter in enumerate(nums):
            if used[i]:
                continue

            path.append(letter)
            used[i] = True
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return results


def permuteUnique(self, nums: List[int]) -> List[List[int]]:
    result = []
    nums.sort()
    n = len(nums)
    visited = [False] * len(nums)

    def backtrack(path):
        if len(path) == n:
            result.append(path[:])
            return

        for i in range(len(nums)):
            if visited[i]:
                continue

            if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                continue

            visited[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            visited[i] = False

    backtrack([])
    return result


def rotate_matrix(
    self, matrix: List[List[int]]
) -> None:  # Do not return anything, modify matrix in-place instead.
    n = len(matrix)

    # Step 1: Transpose the matrix (swap matrix[i][j] with matrix[j][i])
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for row in matrix:
        row.reverse()


def jump(self, nums: List[int]) -> int:
    n = len(nums)
    if n == 1:
        return 0

    jumps, curr_end, farthest = 0, 0, 0

    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])

        if i == curr_end:
            jumps += 1
            curr_end = farthest

            if curr_end >= n - 1:
                break
    return jumps


def maxSubArray(self, nums: List[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)  # extend or start fresh
        best = max(best, cur)
    return best


def findLongestWord(self, s: str, dictionary: List[str]) -> str:
    def is_subseq(word, s):
        i = 0
        for ch in s:
            if i < len(word) and word[i] == ch:
                i += 1
        return i == len(word)

    dictionary.sort(key=lambda w: (-len(w), w))
    for w in dictionary:
        if is_subseq(w, s):
            return w
    return ""


def findErrorNums(self, nums: List[int]) -> List[int]:
    seen = set()
    dup = -1
    for x in nums:
        if x in seen:
            dup = x
        else:
            seen.add(x)
    n = len(nums)
    total = n * (n + 1) // 2
    missing = total - (sum(nums) - dup)
    return [dup, missing]


def joinOverlappingTuples(self, pairs: List[List[int]]) -> int:
    sorted_pairs = sorted(pairs)
    merged = []
    for p in sorted_pairs:
        if not merged or merged[-1][1] < p[0]:
            merged.append(p)
        else:
            merged[-1][1] = max(merged[-1][1], p[1])
    return len(merged)


def replaceWords(self, dictionary: List[str], sentence: str) -> str:
    roots = set(dictionary)

    def shortest_root(word):
        for i in range(1, len(word) + 1):
            pref = word[:i]
            if pref in roots:
                return pref
        return word

    return " ".join(shortest_root(w) for w in sentence.split())


def findLongestChain(self, pairs: List[List[int]]) -> int:
    pairs.sort(key=lambda x: x[1])
    count = 0
    curr_end = float("-inf")
    for a, b in pairs:
        if a > curr_end:
            count += 1
            curr_end = b
    return count


def findKClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
    n = len(arr)
    right = bisect_left(arr, x)
    left = right - 1

    for _ in range(k):
        if left < 0:
            right += 1
        elif right >= n:
            left -= 1
        else:
            if x - arr[1] <= arr[right] - x:
                left -= 1
            else:
                right += 1
    return arr[left + 1 : right]


def checkPossibilityNonDecreasingArray(self, nums: List[int]) -> bool:
    changed = False
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            if changed:
                return False
            changed = True
            # decide whether to lower nums[i] or raise nums[i+1]
            if i == 0 or nums[i - 1] <= nums[i + 1]:
                nums[i] = nums[i + 1]
            else:
                nums[i + 1] = nums[i]
    return True


def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
    if not matrix or not matrix[0]:
        return []
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # left → right
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        # top ↓ bottom
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1

        if top <= bottom:
            # right ← left
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1

        if left <= right:
            # bottom ↑ top
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res


def isMatch(self, s: str, p: str) -> bool:
    i, j = 0, 0  # indices in s and p
    star, i_star = -1, -1  # last '*' position in p and matched index in s

    while i < len(s):
        # exact match or '?'
        if j < len(p) and (p[j] == s[i] or p[j] == "?"):
            i += 1
            j += 1
        # record star and try to match empty sequence
        elif j < len(p) and p[j] == "*":
            star = j
            i_star = i
            j += 1
        # mismatch: backtrack to last star, let it absorb one more char
        elif star != -1:
            j = star + 1
            i_star += 1
            i = i_star
        else:
            return False

        while j < len(p) and p[j] == "*":
            j += 1

        return j == len(p)


def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
    anagrams = defaultdict(list)
    res = []
    for s in strs:
        key = "".join(sorted(s))
        anagrams[key].append(s)

    return list(anagrams.values())


# Sliding Window
def sliding_window(s):
    left = 0
    window = {}  # char -> freq (or any state you maintain)
    best = 0

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1

        # shrink while invalid
        while not is_valid(window):  # define your validity
            lc = s[left]
            window[lc] -= 1
            if window[lc] == 0:
                window.pop(lc)
            left += 1

        best = max(best, right - left + 1)
    return best


# Time: O(n) typical; Space: O(Σ)

# Top-K Elements
import heapq


def top_k(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap  # unsorted top k


# Time: O(n log k), Space: O(k)


# Merge Intervals
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for s, e in intervals:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)
    return merged


# Time: O(n log n), Space: O(1) extra (in-place sort)


# DFS (graph)
from collections import defaultdict


def dfs_graph(n, edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    seen = set()

    def dfs(u):
        seen.add(u)
        for v in g[u]:
            if v not in seen:
                dfs(v)

    for u in range(n):
        if u not in seen:
            dfs(u)


# Time: O(n+m), Space: O(n+m) + recursion


# BFS (graph)
from collections import deque, defaultdict


def bfs_shortest(start, target, edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    q = deque([(start, 0)])
    seen = {start}
    while q:
        u, d = q.popleft()
        if u == target:
            return d
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                q.append((v, d + 1))
    return -1


# Time: O(n+m), Space: O(n)


# Island Count (DFS flood fill)
def num_islands(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]

    def dfs(r, c):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < R
                    and 0 <= ny < C
                    and not seen[nx][ny]
                    and grid[nx][ny] == "1"
                ):
                    seen[nx][ny] = True
                    stack.append((nx, ny))

    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and not seen[r][c]:
                seen[r][c] = True
                dfs(r, c)
                count += 1
    return count


# Time: O(R*C), Space: O(R*C)


def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])  # end time
    take, last_end = 0, float("-inf")
    for s, e in intervals:
        if s >= last_end:
            take += 1
            last_end = e
    return take


# Time: O(n log n)


# Backtracking (subsets)
def backtrack(choices):
    res, path = [], []

    def bt(i=0):
        if done(i, path):  # define your stopping condition
            res.append(path[:])
            return
        for choice in next_choices(i, path, choices):  # generate legal choices
            apply(choice, path)  # choose
            bt(i + 1)  # explore
            undo(choice, path)  # unchoose

    bt()
    return res


# Structure template for permutations/combos/constraints
def subsets(nums):
    res, path = [], []

    def bt(i):
        if i == len(nums):
            res.append(path[:])
            return
        bt(i + 1)  # skip nums[i]
        path.append(nums[i])
        bt(i + 1)  # take nums[i]
        path.pop()

    bt(0)
    return res


# Time: O(2^n), Space: O(n)


# Binary Search
def binary_search(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# Time: O(log n)


# Longest Substring Without Repeat
def length_of_longest_substring(s):
    last = {}  # char -> last index
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


# Time: O(n), Space: O(Σ)


# Max Subarray (Kadane)
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


# Time: O(n), Space: O(1)


# Knapsack 0/1
def knapsack_01(weights, values, W):
    dp = [0] * (W + 1)
    for w, val in zip(weights, values):
        for cap in range(W, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + val)
    return dp[W]


# Time: O(nW), Space: O(W)


# Coin Change (min coins)
def coin_change_min(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1


# Time: O(amount * len(coins)), Space: O(amount)


def coin_change_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:  # coin outer → combos not permutations
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


# Time: O(amount * len(coins)), Space: O(amount)


def top_k_frequent(nums, k):
    freq = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])]


# Time: O(n + k log n)


def min_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    end_heap = []  # min-heap of end times
    for s, e in intervals:
        if end_heap and end_heap[0] <= s:
            heapq.heapreplace(end_heap, e)
        else:
            heapq.heappush(end_heap, e)
    return len(end_heap)


# Time: O(n log n)


# Topological Sort
def topo_sort(n, edges):
    g = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1

    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []  # empty => cycle


# Time: O(n+m)
