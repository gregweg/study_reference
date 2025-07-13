from collections import deque


def num_islands(grid):
  if not grid:
    return 0
  
  rows, cols = len(grid), len(grid[0])
  count = 0

  def dfs(r, c):
    if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
      return
    grid[r][c] = '0' # visited
    # visit neighbors
    dfs(r+1, c)
    dfs(r-1, c)
    dfs(r, c+1)
    dfs(r, c-1)

  for r in range(rows):
    for c in range(cols):
      if grid[r][c] == '1':
        count += 1
        dfs(r, c)
  return count


grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]

print(num_islands(grid)) 


def num_islands_bfs(grid):
  if not grid:
    return 0
  
  rows, cols = len(grid), len(grid[0])
  count = 0
  
  def bfs(r, c):
    queue = deque([(r, c)])
    grid[r][c] = '0' # visited
    while queue:
      x, y = queue.popleft()
      for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
          grid[nx][ny] = '0' # visited
          queue.append((nx, ny))
  
  for r in range(rows):
    for c in range(cols):
      if grid[r][c] == '1':
        count += 1
        bfs(r, c)

  return count

grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]

print(num_islands_bfs(grid))  