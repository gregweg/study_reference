from collections import defaultdict
from threading import Lock

class EditCounter:
  def __init__(self):
    self.counts = defaultdict(int)
    self.lock = Lock()
  
  def increment(self, user_id: str) -> None:
    with self.lock:
      self.counts[user_id] += 1
  
  def get_count(self, user_id: str) -> int:
    with self.lock:
      return self.counts[user_id]

counter = EditCounter()
counter.increment("user1")
counter.increment("user2")
print(counter.get_count("user1"))
print(counter.get_count("user2"))
print(counter.get_count("user3"))