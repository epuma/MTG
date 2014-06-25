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

#It asks for a card and prints all of the information for it
def printCardData(magic_obj):
    default_search = ''
    search = raw_input("Enter name of card (Hit RETURN to quit) ") or default_search
    if search != '':
        if search in magic_obj.flatList:
            for item in magic_obj.flatCards[search].attrlist:
                print item + ': ', getattr(magic_obj.flatCards[search], item)
        else:
            print 'Could not find card: "' + search + '" Please try your search again.'
    if search == '':
        print 'Search Cancelled'

printCardData(a)

printSets(a)
#print len(a.keys())
#print a.flat
#print len(a.flat)
#print 'Ancestral Recall' in a.flat
#print a["LEA"]["Air Elemental"].printings
