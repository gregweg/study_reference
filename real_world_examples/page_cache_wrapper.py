import time

class PageService:
  def load_page(self, page_id: str) -> dict:
    return {"page_id": page_id, "content": f"Content of {page_id}"}

class PageCache:
  def __init__(self, service: PageService, ttl_seconds: int = 60):
    self.service = service
    self.ttl = ttl_seconds
    self.cache: Dict[str, tuple] = {} # page_id -> (data, expiry)

    def get_page(self, page_id: str) -> dict:
      now = time.time()
      if page_id in self.cache:
        data, expiry = self.cache[page_id]
        if expiry > now:
          return data
      data = self.service.load_page(page_id)
      self.cache[page_id] = (data, now + self.ttl)
      return data
    
    def invalidate(self, page_id: str) -> None:
      if page_id in self.cache:
        del self.cache[page_id]

service = PageService()
cache = PageCache(service)
print(cache.get_page("page1"))
print(cache.get_page("page1"))
cache.invalidate("page1")
print(cache.get_page("page1"))