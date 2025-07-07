class Block:
    def __init__(self, id, type, content=None, children=None):
        self.id = id
        self.type = type
        self.content = content or ""      # for leaf nodes
        self.children = children or []   # for internal nodes

class CollaborativeDoc:
    def __init__(self):
        self.blocks = {}
        self.root = Block("root", "root", children=[])
      
      def insert_block(self, parent_id, left_id, right_id, new_block):
        parent = self.blocks[parent_id]
        idx = self._find_index_between(parent.children, left_id, right_id)
        parent.children.insert(idx, new_block)
        self.blocks[new_block.id] = new_block

      def delete_block(self, block_id):
        block = self.blocks[block_id]
        block.tombstone = True
      
      def edit_block_content(self, block_id, text_op):
        block = self.blocks[block_id]
        block.content_buffer.apply(text_op)