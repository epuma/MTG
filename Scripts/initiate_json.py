import os
from Classes import Magic
from pprint import pprint

json_file = os.path.abspath('AllSets-x.json')


a = Magic(json_file)

#It asks for a card and prints all of the information for it
def printCardData(magic_obj):
    default_search = ''
    search = raw_input("Enter name of card (Hit RETURN to quit) ") or default_search
    if search != '':
        if search in magic_obj.flatList:
            magic_obj.flatCards[search].printCard()
        else:
            print 'Could not find card: "' + search + '" Please try your search again.'
    if search == '':
        print 'Search Cancelled'

printCardData(a)

#a.printSets()
#print len(a.keys())
#print a["Limited Edition Alpha"]["Air Elemental"].printings
