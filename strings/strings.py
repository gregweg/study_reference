import re
from collections import Counter

def to_camel_case(text):
    text_split = re.split(r"[-_]",text)
    return ''.join([text_split[0]] + [ x.capitalize() for x in text_split[1:]])

def to_jaden_case(string):
    return ' '.join(list(map(str.capitalize, string.split(" "))))

def to_jaden_case(string):
    return ' '.join(word.capitalize() for word in string.split())

def is_pangram(st):
    return len({char.lower() for char in re.sub(r'[^a-zA-Z]', '', st)}) == 26

def find_it(seq): # finds one odd number in a list
    return [k for k, v in Counter(seq).items() if v % 2 == 1][0]

def is_triangle(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return False
    
    return (
        a + b > c and 
        b + c > a and 
        a + c > b
    )

def find_even_index(arr):
    n = len(arr)
    left_pass, right_pass = [0] * n, [0] * n
    left_pass[0] = arr[0]
    for i in range(1, n):
        left_pass[i] = left_pass[i-1] + arr[i]
    right_pass[n-1] = arr[n-1]
    for i in range(n-2, -1, -1):
        right_pass[i] = right_pass[i+1] + arr[i]
    for i in range(n):
        if left_pass[i] == right_pass[i]:
            return i
    return -1

def create_phone_number(n):
    return "({}) {}-{}".format(''.join(map(str, n[0:3])), ''.join(map(str, n[3:6])), ''.join(map(str, n[6:10])))


def likes(names):
    if len(names) == 0:
        return "no one likes this"
    if len(names) == 1:
        return "{} likes this".format(names[0])
    if len(names) == 2:
        return "{} and {} like this".format(names[0], names[1])
    if len(names) == 3:
        return "{}, {} and {} like this".format(names[0], names[1], names[2])
    if len(names) > 3:
        return "{}, {} and {} others like this".format(names[0], names[1], len(names)-2)
    
def valid_braces(string):
    brace_map = {'[':']', '{':'}', '(':')'}
    brace_stack = []
    for b in string:
        if b in ['(','[','{']:
            brace_stack.append(b)
        elif b in [')', ']', '}']:
            if len(brace_stack) == 0:
                return False
            if brace_map[brace_stack.pop()] != b:
                return False
    return len(brace_stack) == 0

def count(string):
    return Counter(string)

def rot13(message):
    lower_letters = 'abcdefghijklmnopqrstuvwxyz'
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ret = ''
    for c in message:
        if c.isupper():
            new_val = upper_letters[(ord(c) - ord('A') + 13) % 26]
            ret += new_val
        
        elif c.islower():
            new_val = lower_letters[(ord(c) - ord('a') + 13) % 26]
            ret += new_val
        else:
            ret += c
    return ret

def spin_words(sentence):
    return ' '.join([word if len(word) < 5 else word[::-1] for word in sentence.split()])