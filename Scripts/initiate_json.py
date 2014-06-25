import os
from Classes import Magic
from pprint import pprint

json_file = os.path.abspath('AllSets-x.json')


a = Magic(json_file)


#a.findCard('Black Lotus')
#a.printSets()
#print len(a.keys())
#print a["Limited Edition Alpha"]["Air Elemental"].printings
