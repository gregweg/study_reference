import itertools

def two_sum(numbers, target):
    nums = {}
    for i, num in enumerate(numbers):
        diff = target - num
        if diff in nums:
            return (nums[diff], i)
        nums[num] = i

def tower_builder(n_floors):
    if n_floors == 0:
        return []
    
    towers = []
    for i in range(1, n_floors+1):
        stars = '*' * (2 * i - 1)
        space = ' ' * (n_floors - i)
        towers.append(space + stars + space)
    return towers

def last_digit(a, b):
    if b == 0:
        return 1
    return pow(a, b, 10)

def order_weight(strng):
    return ' '.join(sorted(strng.split(), key=lambda x: (sum(int(i) for i in str(x)), x)))

def choose_best_sum(t, k, ls):
    possibilities = [sum(x) for x in itertools.combinations(ls, k) if sum(x) <= t ]
    if len(possibilities) == 0:
        return None
    return min(possibilities, key=lambda x: abs(t - x))

def make_readable(seconds):
    SS = seconds % 60
    MM = (seconds % 3600) // 60
    HH = seconds // 3600
    return f"{HH:02}:{MM:02}:{SS:02}"

from collections import Counter
def score(dice):
    counts = Counter(dice)
    score, dice_used, total_dice = 0, 0, 3

    while any(count > 0 for count in counts.values()):
        # Sort dynamically at each step if needed (by count descending)
        for value, count in sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True):
            if count >= 3 and (total_dice - dice_used >= 3):
                if value == 1:
                    score += value * 1000
                else:
                    score += value * 100
                counts[value] -= 3
                dice_used -= 3
            elif count >= 1 and (total_dice - dice_used >= 1):
                if value == 1:
                    score += 100
                elif value == 5:
                    score += 50                    
                counts[value] -= 1
                dice_used -= 1

    return score

def sum_strings(x, y):
    x, y = x.lstrip('0') or '0', y.lstrip('0') or '0'
    x, y = x[::-1], y[::-1]
    
    carry = 0
    result = []
    max_string_len = max(len(x), len(y))
    
    for i in range(max_string_len):
        x_digit = int(x[i]) if i < len(x) else 0
        y_digit = int(y[i]) if i < len(y) else 0
        s = x_digit + y_digit + carry
        result.append(str(s % 10))
        carry = s // 10
    
    if carry > 0:
        result.append(str(carry))
    
    return ''.join(result[::-1])


def islist(A):
    return isinstance(A, list)
def same_structure_as(original,other):
    if islist(original) != islist(other):
        return False
    elif islist(original):
        if len(original) != len(other):
            return False
        for i in range(len(original)):
            if not same_structure_as(original[i], other[i]):
                return False
        return True
    else:
        return True
    

from copy import deepcopy

def pad_board(board):
    if not board or not board[0]:
        return [[0,0],[0,0]]  # tiny empty pad
    rows, cols = len(board), len(board[0])
    out = [[0]*(cols+2)]
    for row in board:
        out.append([0] + row + [0])
    out.append([0]*(cols+2))
    return out

def crop_board(board):
    live = [(i, j) for i, r in enumerate(board) for j, v in enumerate(r) if v]
    if not live:
        return [[]]
    min_i = min(i for i,_ in live)
    max_i = max(i for i,_ in live)
    min_j = min(j for _,j in live)
    max_j = max(j for _,j in live)
    return [row[min_j:max_j+1] for row in board[min_i:max_i+1]]

def count_neighbors(cells, x, y):
    m, n = len(cells), len(cells[0])
    cnt = 0
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            if dx == 0 and dy == 0: 
                continue
            nx, ny = x+dx, y+dy
            if 0 <= nx < m and 0 <= ny < n and cells[nx][ny] == 1:
                cnt += 1
    return cnt

def get_generation(cells, generations):
    cur = cells
    for _ in range(generations):
        # pad each gen so new births at edges are allowed
        cur = pad_board(cur)
        m, n = len(cur), len(cur[0])
        nxt = [[0]*n for _ in range(m)]  # fresh buffer per gen

        for i in range(m):
            for j in range(n):
                live_neighbors = count_neighbors(cur, i, j)
                if cur[i][j] == 1:
                    nxt[i][j] = 1 if (live_neighbors == 2 or live_neighbors == 3) else 0
                else:
                    nxt[i][j] = 1 if live_neighbors == 3 else 0

        # tighten the board for next iteration / final output
        cur = crop_board(nxt)
        # optional: short-circuit if empty
        if not cur or not cur[0]:
            break

    return cur