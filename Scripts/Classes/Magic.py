import json
from Edition import Edition
from Card import Card

class Magic(dict):
    #This is a Class that will create a Magic object give the json database. It is a dictionary where the Key is the Code of the Edition and the Value is an Edition object. 
    
    def __init__(self, json_file):
        json_data = open(json_file)
        dict = json.load(json_data)
        json_data.close()
        
        flat_list = []
        flat_cards = {}
        for k,v in dict.iteritems():
            self[v["name"]] = Edition(v)
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

    #When called this method will ask for user input, if Card is found then its information will be printed, otherwise it will tell you to try again
    def findCard(self, search = ''):
        if search != '':
            if search in self.flatList:
                return self.flatCards[search].printCard()
            else:
                print 'Could not find card: "' + search + '" Please try your search again.'
        else:
            print 'Please enter a Card Name to Search!'

    