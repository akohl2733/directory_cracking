import json
from db import insert_rec

with open("test.json") as f:
    entry = json.load(f)

row_id = insert_rec(entry)

print(f"Insert row with Id {row_id}")