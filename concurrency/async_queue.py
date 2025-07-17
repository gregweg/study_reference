import asyncio

class AsyncReaderWriterLock:
  def __init__(self):
    self._readers = 0
    self._writer = False
    self._cond = asyncio.Condition()
  
  async def acquire_read(self):
    async with self._cond:
      while self._writer:
        await self._cond.wait()
      self._readers += 1
    
  async def release_read(self):
    async with self._cond:
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()
  
  async def acquire_write(self):
     async with self._cond:
        while self._writer or self._readers > 0:
           await self._cond.wait()
        self._writer = True
    
  async def release_write(self):
     async with self._cond:
        self._writer = False
        self._cond.notify_all()

lock = AsyncReaderWriterLock()

async def reader(i):
    await lock.acquire_read()
    print(f"Reader {i} starts reading")
    await asyncio.sleep(1)
    print(f"Reader {i} done")
    await lock.release_read()

async def writer(i):
    await lock.acquire_write()
    print(f"Writer {i} starts writing")
    await asyncio.sleep(2)
    print(f"Writer {i} done")
    await lock.release_write()

async def test_rw_lock():
    await asyncio.gather(
        reader(1),
        reader(2),
        writer(1),
        reader(3),
        writer(2)
    )

if __name__ == "__main__":
    asyncio.run(test_rw_lock())