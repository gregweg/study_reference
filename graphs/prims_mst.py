import heapq

def prim_mst(graph):
  # graph: {node: [(neighbor, weight), ...]}
  start = next(iter(graph))
  visited = set([start])
  edges = [(weight, start, v) for v, weight in graph[start]]
  heapq.heapify(edges)
  mst = []
  total_weight = 0

  while edges:
    weight, u, v = heapq.heappop(edges)
    if v not in visited:
      visited.add(v)
      mst.append((u, v, weight))
      total_weight += weight
      for neighbor, weight in graph[v]:
        if neighbor not in visited:
          heapq.heappush(edges, (weight, v, neighbor))
  return mst, total_weight

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1), ('E', 1)],
    'E': [('D', 1), ('F', 1)],
    'F': [('E', 1)],
}

mst, weight = prim_mst(graph)
print(mst)       # [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 1), ('D', 'E', 1), ('E', 'F', 1)]
print(weight)    # 6

graph_2 = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}

mst, weight = prim_mst(graph_2)
print(mst)       # [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 1)]
print(weight)    # 4