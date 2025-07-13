import heapq

def dijkstras(graph, start):
  distances = {node: float('infinity') for node in graph}
  distances[start] = 0
  priority_queue = [(0, start)]

  while priority_queue:
    current_distance, current_node = heapq.heappop(priority_queue)

    if current_distance > distances[current_node]:
      continue
    for neighbor, weight in graph[current_node]:
      if distances[current_node] + weight < distances[neighbor]:
        distances[neighbor] = distances[current_node] + weight
        heapq.heappush(priority_queue, (distances[neighbor], neighbor))
  return distances

graph_1 = {
  'A': [('B', 1), ('C', 4)],
  'B': [('A', 1), ('C', 2), ('D', 5)],
  'C': [('A', 4), ('B', 2), ('D', 1)],
  'D': [('B', 5), ('C', 1), ('E', 1)],
  'E': [('D', 1), ('F', 1)],
  'F': [('E', 1)],
}

graph_2 = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}
print(dijkstras(graph_1, 'A'))

print(dijkstras(graph_2, 'A'))