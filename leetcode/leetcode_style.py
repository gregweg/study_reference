from typing import List

def can_complete_circuit(gas: List[int], cost: List[int]) -> int:
  if not gas or not cost or len(gas) != len(cost):
    return -1
  
  total = 0
  tank = 0
  start = 0
  
  for i in range(len(gas)):
    diff = gas[i] - cost[i]
    total += diff
    tank += diff
    if tank < 0:
      start = i + 1
      tank = 0
  return start if total >= 0 and start < len(gas) else -1

if __name__ == "__main__":
  assert can_complete_circuit([1,2,3,4,5], [3,4,5,1,2]) == 3 # Example 1: valid start is 3
  assert can_complete_circuit([2,3,4], [3,4,3]) == -1 # Example 2: impossible
  assert can_complete_circuit([5], [5]) == 0 # Edge: exact balance starting at 0
  assert can_complete_circuit([2], [3]) == -1 # Edge: single station with not enough fuel
  assert can_complete_circuit([2,3,4], [1,2,3]) == 0 # Case: multiple stations, valid start at 1
  print("All tests passed")