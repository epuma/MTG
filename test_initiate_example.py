"""
Quick smoke-test for the Classes layer.

Writes output to test_collection_output.json (gitignored) so it never
overwrites the sample eric_collection.json in the repository root.
"""
from Classes import Magic, Collection

JSON_FILE   = 'JSON Files/AllSets-x.json'
OUTPUT_FILE = 'test_collection_output.json'

print(f'Loading {JSON_FILE}…')
db = Magic(JSON_FILE)

print(f'Building collection skeleton → {OUTPUT_FILE}')
coll = Collection()
coll.newCollection(db, OUTPUT_FILE)
coll.load(OUTPUT_FILE)

print(coll)
print('Total quantity:', coll.getTotalQuantity())
print('Total price:   ', coll.getTotalPrice())
print('Done.')
