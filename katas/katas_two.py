
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

class RomanNumerals:
    roman_map = [
        (1000, 'M'), (900, 'CM'),
        (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'),
        (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'),
        (5, 'V'), (4, 'IV'),
        (1, 'I')
    ]
    
    @staticmethod
    def to_roman(val : int) -> str:
        result = []
        for num, symbol in RomanNumerals.roman_map:
            while val >= num:
                result.append(symbol)
                val -= num
        return ''.join(result)

    @staticmethod
    def from_roman(roman_num : str) -> int:
        index = 0
        result = 0
        for num, symbol in RomanNumerals.roman_map:
            while roman_num[index:index + len(symbol)] == symbol:
                result += num
                index += len(symbol)
        return result
    
def hamming(n):
    if n <= 0:
        raise ValueError("n must be positive")

    h = [1] * n  # h[0] = 1 is the first Hamming number
    i2 = i3 = i5 = 0  # pointers to the next factors 2, 3, 5

    for t in range(1, n):
        next2, next3, next5 = 2 * h[i2], 3 * h[i3], 5 * h[i5]
        x = min(next2, next3, next5)
        h[t] = x
        if x == next2: i2 += 1
        if x == next3: i3 += 1
        if x == next5: i5 += 1

    return h[-1]

import re

def decode_bits(bits):
    bits = bits.strip('0')
    if not bits:
        return ''
    runs = re.findall(r'(1+|0+)', bits)
    min_unit = min(len(run) for run in runs)
    
    normalized = ''.join(
        ('1' * (len(run)//min_unit) if run[0] == '1' else '0' * (len(run)//min_unit))
        for run in runs
    )
    
    morse = normalized
    morse = morse.replace('000000', '   ')
    morse = morse.replace('000', ' ')
    morse = morse.replace('111', '-')
    morse = morse.replace('1', '.')
    morse = morse.replace('0', '')
    return morse
    

def decode_morse(morseCode):
    words = morseCode.strip().split('   ')
    decoded_words = []
    for word in words:
        letters = [MORSE_CODE.get(symbol, '') for symbol in word.split()]
        decoded_words.append(''.join(letters))
    return ' '.join(decoded_words)

MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D',
    '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
    '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
    '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '-.-.--': '!',
    '-....-': '-', '-..-.': '/', '.--.-.': '@', '-.--.': '(', '-.--.-': ')'
}