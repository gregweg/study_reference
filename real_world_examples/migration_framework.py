from typing import Callable, List, Dict

def migrate(records: List[Dict], transform_fn: Callable[[Dict], Dict]) -> List[Dict]:
  return [transform_fn(record) for record in records]

def example_transform(record: Dict) -> Dict:
  return {
    "user_id": record["id"],
    "full_name": record["name"]
  }

old_records = [
  {"id": 1, "name": "John Doe"},
  {"id": 2, "name": "Jane Smith"},
  {"id": 3, "name": "Alice Johnson"}
]

new_records = migrate(old_records, example_transform)
print(new_records)
# [{'user_id': 1, 'full_name': 'John Doe'}, {'user_id': 2, 'full_name': 'Jane Smith'}, {'user_id': 3, 'full_name': 'Alice Johnson'}]