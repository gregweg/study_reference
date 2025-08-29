from preloaded import htmlize # this can help you debug your code
from copy import deepcopy

def pad_board(board):
    rows, cols = len(board), len(board[0])
    new_board = [[0] * (cols + 2)]
    for row in board:
        new_board.append([0] + row + [0])
    new_board.append([0] * (cols + 2))
    return new_board

def crop_board(board):
    live_cells = [(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val]
    if not live_cells:
        return [[]]
    
    min_x = min(x for x, y in live_cells)
    max_x = max(x for x, y in live_cells)
    min_y = min(y for x, y in live_cells)
    max_y = max(y for x, y in live_cells)
    
    return [row[min_y:max_y+1] for row in board[min_x:max_x+1]]

def get_neighbors(x, y):
    return [
        (x-1, y-1), (x-1, y), (x-1, y+1),
        (x, y-1),           (x, y+1),
        (x+1, y-1), (x+1, y), (x+1, y+1)
    ]
def count_neighbors(cells : list[list[int]], x : int, y : int):
    neighbor_count = 0
    m, n = len(cells), len(cells[0])
    for nx, ny in get_neighbors(x, y):
        if nx >= 0 and ny >= 0 and nx < m and ny < n and cells[nx][ny] == 1:
            neighbor_count += 1
    return neighbor_count

def get_generation(cells : list[list[int]], generations : int) -> list[list[int]]:
    cells = pad_board(cells)
    m, n = len(cells), len(cells[0])
    print(f"m: {m} n: {n}")
    print(htmlize(cells))
    new_cells = deepcopy(cells)
    
    
    for _ in range(generations):
        for i in range(m):
            for j in range(n):
                live_neighbors = count_neighbors(cells, i, j)
                if cells[i][j] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_cells[i][j] = 0
                    else:
                        new_cells[i][j] = 1
                else:
                    if live_neighbors == 3:
                        new_cells[i][j] = 1
        print(htmlize(new_cells))
        cells = crop_board(new_cells)
        print(htmlize(cells))
    return cells