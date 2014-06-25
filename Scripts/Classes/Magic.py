from Edition import Edition
from Card import Card

class Magic(dict):
    #This is a class that will create a Magic object give the json database. It is a dictionary where the Key is the Code of the Edition and the Value is an Edition object. 
    
    def __init__(self, dict):
        flat_list = []
        flat_cards = {}
        for k,v in dict.iteritems():
            self[k] = Edition(v)
            for stuff in v["cards"]:
                flat_list.append(stuff["name"])
                flat_cards[stuff["name"]] = Card(stuff)
        self.flatList = sorted(list(set(flat_list)))
        self.flatCards = flat_cards

    #prints Set names and releaseDates
    def printSets(self):
        d = {}
        for k,v in self.iteritems():
            d[v.name] = v.releaseDate
        sorted_d = sorted(d, key=lambda key: d[key])

        for item in sorted_d:
            print item, d[item]