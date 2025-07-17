import threading

class ThreadSafeQueue:
  def __init__(self):
    self.queue = []
    self.lock = threading.Lock()
  
  def enqueue(self, item):
    with self.lock:
      self.queue.append(item)
    
  def dequeue(self):
    with self.lock:
      if self.queue:
        return self.queue.pop(0)
      return None

  def is_empty(self):
    with self.lock:
      return len(self.queue) == 0
    
