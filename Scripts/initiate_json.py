from Classes import Magic
from Classes import lib
from Classes import Collection

json_file = 'AllSets-x.json'

a = Magic(json_file)

#this next section starts on creating a collection give a MAGIC Object and writing it to a JSON



b = Collection.Collection()
#b.newCollection(a, 'eric_collection.json')
b.load('eric_collection.json')

b.addCard('Limited Edition Alpha', 'Black Lotus', 1)

b.save('eric_collection.json')

print b.getQuantity('Limited Edition Alpha', 'Black Lotus')

print b

#print a.findCard('AEther Spellbomb')

#print a
#print len(a.keys())
#print a["Limited Edition Alpha"]["Air Elemental"].printings
