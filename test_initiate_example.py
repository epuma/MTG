from Classes import Magic
from Classes import Collection

json_file = 'JSON Files/AllSets-x.json'

a = Magic(json_file)

#this next section starts on creating a collection give a MAGIC Object and writing it to a JSON


#b = Collection.Collection()
#b.newCollection(a, 'eric_collection.json')
#b.load('eric_collection.json')
#b.updateCollection(a)

#print b.getQuantity('Limited Edition Alpha', 'Black Lotus')

#print a.findCard('AEther Spellbomb')

print sorted(a.data.keys())
#print a["Limited Edition Alpha"]["Air Elemental"].printings