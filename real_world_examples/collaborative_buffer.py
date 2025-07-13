class UserRepository:
    def __init__(self, db):
        self.db = db
    def find_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

# Service Layer
class AuthService:
    def __init__(self, user_repo):
        self.repo = user_repo
    def login(self, email, password):
        user = self.repo.find_by_email(email)
        return check_password(user, password)
    
class Engine:
    def start(self): print("Engine started")
class Car:
    def __init__(self):
        self.engine = Engine()
    def drive(self):
        self.engine.start()
        print("Car is driving")


# Design a Data Model for a Page  that supports nested blocks, toggles, and inline databases.

# Implement undo/redo for editing a rich-text document or blcok-based content tree

# Model a real-time collaborative edting buffer, merging changes from multiple users with conflict resolution.


from dataclasses import dataclass

@dataclass(order=True)
class Char:
    id: tuple   # (site_id, counter)
    value: str
    tombstone: bool = False
from typing import List, Optional
class CollaborativeBuffer:
    def __init__(self, site_id):
        self.site_id = site_id
        self.counter = 0
        self.chars: List[Char] = []

    def insert(self, pos, value):
        self.counter += 1
        new_id = (self.site_id, self.counter)
        char = Char(new_id, value)
        self.chars.insert(pos, char)
        return ('insert', char)
    
    def delete(self, pos):
        self.chars[pos].tombstone = True
        return ('delete', self.chars[pos].id)

    def apply(self, op):
        if op[0] == 'insert':
            char = op[1]
            self.chars.append(char)
            self.chars.sort()
        elif op[0] == 'delete':
            id_to_delete = op[1]
            for c in self.chars:
                if c.id == id_to_delete:
                    c.tombstone = True
                    break
    
    def render(self):
        return ''.join(c.value for c in self.buffer if not c.tombstone)
    
doc1 = CollaborativeBuffer(site_id=1)
doc2 = CollaborativeBuffer(site_id=2)

# User 1 inserts 'H'
op1 = doc1.insert(0, 'H')
doc2.apply(op1)

# User 2 inserts 'i' after 'H'
op2 = doc2.insert(1, 'i')
doc1.apply(op2)

print(doc1.render())  # Hi
print(doc2.render())  # Hi
