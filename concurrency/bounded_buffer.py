import threading
import queue
import time
import random

buffer = queue.Queue(maxsize=10)

def producer():
  while True:
    item = random.randint(0, 100)
    buffer.put(item)
    print(f"Produced: {item}")
    time.sleep(random.random())

def consumer():
  while True:
    item = buffer.get()
    print(f"Consumed: {item}")
    buffer.task_done()
    time.sleep(random.random())


threads = []
for _ in range(2):
  t = threading.Thread(target=producer)
  t.start()
  threads.append(t)

for _ in range(2):
  t = threading.Thread(target=consumer)
  t.start()
  threads.append(t)

for t in threads:
  t.join()
