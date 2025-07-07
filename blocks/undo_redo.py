from dataclasses import dataclass, field
from typing import List, Optional
import copy


# -----------------------------
# Data Classes
# -----------------------------

@dataclass
class Block:
    id: str
    type: str
    content: str
    children: List["Block"] = field(default_factory=list)


@dataclass
class Operation:
    type: str  # "insert", "delete", "update"
    block: Optional[Block] = None
    block_id: Optional[str] = None
    parent_id: Optional[str] = None
    prev_content: Optional[str] = None
    new_content: Optional[str] = None
    index: Optional[int] = None


# -----------------------------
# Tree Helpers
# -----------------------------

def find_block_by_id(blocks: List[Block], block_id: str) -> Optional[Block]:
    for block in blocks:
        if block.id == block_id:
            return block
        found = find_block_by_id(block.children, block_id)
        if found:
            return found
    return None


def insert_block(blocks: List[Block], parent_id: Optional[str], new_block: Block, index: int):
    if parent_id is None:
        blocks.insert(index, new_block)
    else:
        parent = find_block_by_id(blocks, parent_id)
        if parent:
            parent.children.insert(index, new_block)


def delete_block(blocks: List[Block], block_id: str) -> Optional[Block]:
    for i, block in enumerate(blocks):
        if block.id == block_id:
            return blocks.pop(i)
        deleted = delete_block(block.children, block_id)
        if deleted:
            return deleted
    return None


def update_content(blocks: List[Block], block_id: str, new_content: str) -> Optional[str]:
    block = find_block_by_id(blocks, block_id)
    if block:
        old = block.content
        block.content = new_content
        return old
    return None


# -----------------------------
# Undo/Redo Management
# -----------------------------

undo_stack: List[Operation] = []
redo_stack: List[Operation] = []


def inverse(op: Operation) -> Operation:
    if op.type == "insert":
        return Operation(type="delete", block_id=op.block.id, parent_id=op.parent_id, block=op.block)
    elif op.type == "delete":
        return Operation(type="insert", block=op.block, parent_id=op.parent_id, index=op.index)
    elif op.type == "update":
        return Operation(type="update", block_id=op.block_id, prev_content=op.new_content, new_content=op.prev_content)
    raise ValueError("Unknown operation type")


def apply_operation(op: Operation, tree: List[Block]):
    if op.type == "insert":
        insert_block(tree, op.parent_id, copy.deepcopy(op.block), op.index)
    elif op.type == "delete":
        deleted = delete_block(tree, op.block_id)
        op.block = deleted
    elif op.type == "update":
        prev = update_content(tree, op.block_id, op.new_content)
        op.prev_content = prev


def do_operation(op: Operation, tree: List[Block]):
    apply_operation(op, tree)
    undo_stack.append(inverse(op))
    redo_stack.clear()


def undo(tree: List[Block]):
    if not undo_stack:
        print("Nothing to undo.")
        return
    op = undo_stack.pop()
    apply_operation(op, tree)
    redo_stack.append(inverse(op))


def redo(tree: List[Block]):
    if not redo_stack:
        print("Nothing to redo.")
        return
    op = redo_stack.pop()
    apply_operation(op, tree)
    undo_stack.append(inverse(op))


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    tree: List[Block] = []

    # Insert Block 1
    b1 = Block(id="1", type="paragraph", content="Hello world")
    do_operation(Operation(type="insert", block=b1, parent_id=None, index=0), tree)

    # Insert Block 2
    b2 = Block(id="2", type="paragraph", content="Second block")
    do_operation(Operation(type="insert", block=b2, parent_id=None, index=1), tree)

    # Update Block 1
    do_operation(Operation(type="update", block_id="1", new_content="Hello Notion"), tree)

    # State before undo
    print("\nBefore Undo:")
    for b in tree:
        print(f"{b.id}: {b.content}")

    # Undo the update
    undo(tree)

    print("\nAfter Undo:")
    for b in tree:
        print(f"{b.id}: {b.content}")

    # Redo the update
    redo(tree)

    print("\nAfter Redo:")
    for b in tree:
        print(f"{b.id}: {b.content}")