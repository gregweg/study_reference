def topological_sort(graph):
  visited = set()
  stack = []

  def dfs(node):
    visited.add(node)
    for neighbor in graph[node]:
      if neighbor not in visited:
        dfs(neighbor)
    stack.append(node)

  for node in graph:
    if node not in visited:
      dfs(node)
  return stack[::-1] # reverse stack

graph = {
  'A': ['B', 'C'],
  'B': ['D'],
  'C': ['D', 'E'],
  'D': ['F'],
  'E': ['F'],
  'F': []
}

print(topological_sort(graph))