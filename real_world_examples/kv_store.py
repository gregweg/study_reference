class KVStore:
  def __init__(self):
    self.store = {}

  def get(self, key: str) -> Optional[str]:
    return self.store.get(key)
  
  def set(self, key: str, value: str) -> None:
    self.store[key] = value

def toggle_block(block_id: str, store: KVStore) -> bool:
  current = store.get(block_id)
  if current == "collapsed":
    store.set(block_id, "expanded")
  else:
    store.set(block_id, "collapsed")
  return True

store = KVStore()
toggle_block("block123", store)
print(store.get("block123")) # collapsed
toggle_block("block123", store)
print(store.get("block123")) # expanded
