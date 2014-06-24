from Classes import Magic
import json
from pprint import pprint

json_data = open('AllSets-x.json')
data = json.load(json_data)
json_data.close()

a = Magic(data)

#prints Set names and releaseDates

def printSets(magic_obj):
    d = {}
    for k,v in magic_obj.iteritems():
        d[v.name] = v.releaseDate
    sorted_d = sorted(d, key=lambda key: d[key])

    for item in sorted_d:
        print item, d[item]

#printSets(a)
#print len(a.keys())
print a.flat
print len(a.flat)
#print a["LEA"]["Air Elemental"].printings
