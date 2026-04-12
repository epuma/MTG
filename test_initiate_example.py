from Classes import Magic, Collection

json_file = 'JSON Files/AllSets-x.json'

a = Magic(json_file)

b = Collection()
b.newCollection(a, 'eric_collection.json')
b.load('eric_collection.json')

print(b)
print(b.getTotalQuantity())
print(b.getTotalPrice())
