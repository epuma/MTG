from Classes import Magic

json_file = 'AllSets-x.json'

a = Magic(json_file)

#this next section starts on creating a collection give a MAGIC Object and writing it to a JSON
import io, json
b = {}
for sets in a.keys():
    for k,v in a[sets].iteritems():
        b[sets].update({k:0})

with open('eric_collection.json', 'w') as outfile:
    json.dump(b, outfile)








a.findCard('Black Lotus')
#a.printSets()
#print len(a.keys())
#print a["Limited Edition Alpha"]["Air Elemental"].printings
