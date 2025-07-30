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