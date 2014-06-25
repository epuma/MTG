from Classes import Magic
import json
from pprint import pprint

json_data = open('AllSets-x.json')
data = json.load(json_data)
json_data.close()

a = Magic(data)

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

#printCardData(a)

a.printSets()

#print len(a.keys())
#print a.flat
#print len(a.flat)
#print 'Ancestral Recall' in a.flat
#print a["LEA"]["Air Elemental"].printings
