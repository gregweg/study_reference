
# 🐍 Python Interview Reference Sheet

# Functions and Lambdas
def greet(name: str) -> str:
    return f"Hello, {name}"

square = lambda x: x * x

# List Comprehensions
squares = [x*x for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]

# Dict/Set Comprehensions
char_map = {char: ord(char) for char in 'abc'}
unique_vals = {val for val in [1, 2, 2, 3]}

## 🔹 2. OOP + Code Abstraction

# Tuple (immutable, hashable)
t = (1, 2, 3)
a, b, c = t

# Set (unique unordered values)
s = set([1, 2, 2, 3])
s.add(4)

# Dict (hash map)
d = {'a': 1, 'b': 2}
d.get('c', 0)

# defaultdict (auto-create default values)
from collections import defaultdict
freq = defaultdict(int)
for char in "aabbbc":
    freq[char] += 1

# deque (fast appends/pops on both ends)
from collections import deque
q = deque()
q.append(1)
q.appendleft(0)
q.pop()
q.popleft()

# heapq (min-heap)
import heapq
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
min_val = heapq.heappop(heap)

# Counter (multiset)
from collections import Counter
c = Counter("aabbbc")
most_common = c.most_common(2)

# bisect (binary search)
import bisect
sorted_list = [1, 2, 3, 4, 5]
bisect.bisect_left(sorted_list, 3)


# Abstract Classes
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float): pass

class StripeProcessor(PaymentProcessor):
    def charge(self, amount):
        print(f"Charging ${amount} via Stripe")

# Factory Example
def get_processor(provider: str) -> PaymentProcessor:
    return StripeProcessor() if provider == "stripe" else OtherProcessor()


# Composition over Inheritance
class Engine:
    def start(self): print("Engine started")
class Car:
    def __init__(self):
        self.engine = Engine()
    def drive(self):
        self.engine.start()
        print("Car is driving")

# Strategy Pattern
class SortStrategy:
    def sort(self, data): raise NotImplementedError
class QuickSort(SortStrategy):
    def sort(self, data): return sorted(data)
class BubbleSort(SortStrategy):
    def sort(self, data): return data  # Stub for example
class Context:
    def __init__(self, strategy): self.strategy = strategy
    def execute(self, data): return self.strategy.sort(data)

# Encapsulation and Invariants
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance
    def deposit(self, amount):
        if amount > 0: self._balance += amount
    def withdraw(self, amount):
        if 0 < amount <= self._balance: self._balance -= amount


# Squares of numbers from 0 to 9
squares = [x**2 for x in range(10)]

# Even numbers from 0 to 9
evens = [x for x in range(10) if x % 2 == 0]

# Flatten a 2D list
matrix = [[1, 2], [3, 4]]
flattened = [num for row in matrix for num in row]

# Extract digits from a string
digits = [int(ch) for ch in "a1b2c3" if ch.isdigit()]

# Create a dictionary from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
kv_dict = {k: v for k, v in zip(keys, values)}

# Filter and transform items in one pass
names = ["alice", "bob", "charlie"]
capitalized = [name.capitalize() for name in names if len(name) > 3]

# Remove None values
data = [1, None, 2, None, 3]
cleaned = [x for x in data if x is not None]

# Transpose a matrix
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]


## 🔹 4. Performance + Caching

# Memoization
from functools import lru_cache

@lru_cache(maxsize=1000)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# In-Memory Cache
cache = {}

def get_user(id):
    if id in cache:
        return cache[id]
    user = db_query(id)
    cache[id] = user
    return user

## 🔹 5. Design Patterns

# Repository Pattern
class UserRepository:
    def __init__(self, db):
        self.db = db
    def find_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

# Service Layer
class AuthService:
    def __init__(self, user_repo):
        self.repo = user_repo
    def login(self, email, password):
        user = self.repo.find_by_email(email)
        return check_password(user, password)


# Heap for Top-K
import heapq
def top_k(nums, k):
    return heapq.nlargest(k, nums)

# Sliding Window
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(len(arr) - k):
        window_sum += arr[i + k] - arr[i]
        max_sum = max(max_sum, window_sum)
    return max_sum

# Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


## 2. Graph Search

# DFS (recursive)
def dfs(node, visited, graph):
    if node in visited: return
    visited.add(node)
    for neighbor in graph[node]:
        dfs(neighbor, visited, graph)

# BFS (queue-based)
from collections import deque
def bfs(start, graph):
    visited = set([start])
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


# Two Pointers
def has_pair_sum(nums, target):
    nums.sort()
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target: return True
        elif s < target: l += 1
        else: r -= 1
    return False

# Merge Intervals
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for curr in intervals[1:]:
        if curr[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], curr[1])
        else:
            merged.append(curr)
    return merged

## 3. Greedy Algorithms

# Activity selection (earliest end time first)
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])
    count, end = 0, float('-inf')
    for start, finish in intervals:
        if start >= end:
            count += 1
            end = finish
    return count

# Huffman Coding (example of greedy with heap)
# Use frequency map to build optimal prefix code (not shown here)

## 4. Other Common Patterns

# Union-Find (Disjoint Set)
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

# Topological Sort (Kahn's Algorithm)
def topological_sort(graph):
    indegree = defaultdict(int)
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1
    q = deque([u for u in graph if indegree[u] == 0])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for v in graph[node]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    return order if len(order) == len(graph) else []

# Sliding Window
def longest_substring_k_distinct(s, k):
    from collections import defaultdict
    count = defaultdict(int)
    left = max_len = 0
    for right in range(len(s)):
        count[s[right]] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len

## 5. Dynamic Programming (DP)

# Fibonacci with memoization
def fib_dp(n):
    if n < 2:
        return n
    dp = [0, 1]
    for i in range(2, n+1):
        dp.append(dp[i-1] + dp[i-2])
    return dp[n]

# 0/1 Knapsack
def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0] * (W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w-weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]

# Longest Increasing Subsequence
def lis(arr):
    if not arr:
        return 0
    dp = [1] * len(arr)
    for i in range(len(arr)):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j]+1)
    return max(dp)

# Asteroid Collision
def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        while stack and a < 0 and stack[-1] > 0:
            if abs(stack[-1]) < abs(a):
                stack.pop()
                continue
            elif abs(stack[-1]) == abs(a):
                stack.pop()
            break
        else:
            stack.append(a)
    return stack

## 7. Concurrency and Parallelism

import threading

# Using threading
def task(name):
    print(f"Task {name} running")
threads = [threading.Thread(target=task, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()

# Thread-safe counter
from threading import Lock

class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = Lock()
    def increment(self):
        with self.lock:
            self.count += 1

# concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def square(n): return n * n
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(square, range(10)))

# asyncio (asynchronous I/O)
import asyncio

async def fetch_data(n):
    await asyncio.sleep(1)
    return f"Result {n}"

async def main():
    results = await asyncio.gather(fetch_data(1), fetch_data(2))
    print(results)

# Run: asyncio.run(main())


# Timing
import time

start = time.perf_counter()
# do_work()
print("Elapsed:", time.perf_counter() - start)

## 🔹 3. Testing (with pytest)

# Basic Unit Test
def test_add():
    assert add(2, 3) == 5

# Mocking
from unittest.mock import patch

@patch('email_service.send_email')
def test_checkout_sends_email(mock_send):
    checkout()
    mock_send.assert_called_once()

def mostVisitedPattern(self, username: List[str], timestamp: List[int], website: List[str]) -> List[str]:
    visited = sorted(zip(username, timestamp, website))

    user_to_website = defaultdict(list)
    for user, time, website in visited:
        user_to_website[user].append(website)
        
    pattern_to_users = defaultdict(set)
    for user, websites in user_to_website.items():
        patterns = set(combinations(websites, 3))
        for pattern in patterns:
            pattern_to_users[pattern].add(user)
        
    max_score = 0
    result_pattern = None
    for pattern, users in pattern_to_users.items():
        score = len(users)
        if score > max_score or (score == max_score and (result_pattern is None or pattern < result_pattern)):
            max_score = score
            result_pattern = pattern
    return list(result_pattern)

def exist(self, board: List[List[str]], word: str) -> bool:
    # IF len of board or 
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False
            
        temp = board[r][c]
        board[r][c] = '#'

        found = (dfs(r+1, c, idx+1) or
                dfs(r-1, c, idx+1) or
                dfs(r, c+1, idx+1) or
                dfs(r, c-1, idx+1))
        
        board[r][c] = temp
            
        return found
        
    for i in range(rows):
        for j in range(cols):
            if dfs(i, j, 0):
                return True
        
    return False

def shipWithinDays(self, weights: List[int], days: int) -> int:
        def days_needed(capacity):
            d = 1
            total = 0
            for w in weights:
                if total + w > capacity:
                    d += 1
                    total = 0
                total += w
            return d
        
        left, right = max(weights), sum(weights)
        result = right

        while left <= right:
            mid = (left + right) // 2
            if days_needed(mid) <= days:
                result = mid
                right = mid - 1
            else:
                left = mid + 1
        return result