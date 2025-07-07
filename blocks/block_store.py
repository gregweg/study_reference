from typing import List, Optional, Dict
import uuid

class Block:
  def __init__(self, block_type: str, content: str, block_id: Optional[str] = None):
    self.id: str = block_id or str(uuid.uuid4())
    self.type: str = block_type
    self.content: str = content
    self.children: List["Block"] = []
  
  def __repr__(self):
    return f"Block(id={self.id}, type={self.type}, content={self.content})"
  
class BlockStore:
  def __init__(self):
    self.root = Block("root", "Document Root")
  
  def find_block(self, block_id: str, current: Optional[Block] = None) -> Optional[Block]:
    if current is None:
      current = self.root
      
    if current.id == block_id:
      return current
    
    for child in current.children:
      found = self.find_block(block_id, child)
      if found:
        return found
      
    return None
    
  def add_block(self, parent_id: str, block: Block, position: Optional[int] = None) -> bool:
    parent = self.find_block(parent_id)
    if not parent:
      return False
    if position is None or position >= len(parent.children):
      parent.children.append(block)
    else:
      parent.children.insert(position, block)
    return True
  
  def delete_block(self, block_id: str, current: Optional[Block] = None) -> bool:
    if current is None:
      current = self.root
    for idx, child in enumerate(current.children):
      if child.id == block_id:
        del current.children[idx]
        return True
      if self.delete_block(block_id, child):
        return True
    return False
  
  def move_block(self, block_id: str, new_parent_id: str, position: Optional[int] = None) -> bool:
    block = self.find_block(block_id)
    if not block:
      return False
    # Remove block from the current parent
    if not self.delete_block(block_id):
      return False
    # Add the block to the new parent
    return self.add_block(new_parent_id, block, position)
  
  def edit_block_content(self, block_id: str, new_content: str) -> bool:
    block = self.find_block(block_id)