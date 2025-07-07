import unittest
from block_store import BlockStore, Block

class TestBlockStore(unittest.TestCase):
  def setUp(self):
    self.block_store = BlockStore()
    self.block_a = Block("paragraph", "A")
    self.block_b = Block("heading", "B")
    self.block_c = Block("list", "C")
    self.block_store.add_block(self.block_store.root.id, self.block_a)
    self.block_store.add_block(self.block_store.root.id, self.block_b)

  def test_add_block(self):
    self.assertEqual(len(self.block_store.root.children), 2)
    self.block_store.add_block(self.block_a.id, self.block_c)
    self.assertEqual(len(self.block_a.children), 1)
    self.assertEqual(self.block_a.children[0].content, "C")

  def test_delete_block(self):
     self.assertTrue(self.block_store.delete_block(self.block_a.id))
     self.assertIsNone(self.block_store.find_block(self.block_a.id))
     self.assertEqual(len(self.block_store.root.children), 1)

  def test_move_block(self):
     self.block_store.add_block(self.block_store.root.id, self.block_c)
     self.assertTrue(self.block_store.move_block(self.block_c.id, self.block_a.id))
     self.assertIn(self.block_c, self.block_a.children)
     self.assertNotIn(self.block_c, self.block_store.root.children)
  
  def test_find_block(self):
     found = self.block_store.find_block(self.block_a.id)
     self.assertEqual(found.content, "A")
     self.assertIsNone(self.block_store.find_block("non_existent_id"))

if __name__ == "__main__":
    unittest.main()