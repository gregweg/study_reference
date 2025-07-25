import asyncio
import random

async def producer(queue):
  while True:
    item = random.randint(1, 100)
    await queue.put(item)
    print(f"Produced: {item}")
    await asyncio.sleep(random.random())

async def consumer(queue):
  while True:
    item = await queue.get()
    print(f"Consumed: {item}")
    queue.task_done()
    await asyncio.sleep(random.random())

async def main():
  queue = asyncio.Queue(maxsize=5)

  producer_task = [asyncio.create_task(producer(queue)) for _ in range(2)]
  consumer_task = [asyncio.create_task(consumer(queue)) for _ in range(2)]

  await asyncio.gather(*producer_task, *consumer_task)


async def test_producer_consumer():
  task = asyncio.create_task(main())
  await asyncio.sleep(5)
  task.cancel()

if __name__ == "__main__":
  asyncio.run(test_producer_consumer())