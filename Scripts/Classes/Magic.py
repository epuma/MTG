import json
from Edition import Edition
from Card import Card
from lib import clean_unicode

class Magic(object):
    #This is a Class that will create a Magic object give the json database. It is a dictionary where the Key is the Code of the Edition and the Value is an Edition object. 
    
    def __init__(self, json_file):
        json_data_file = open(json_file)
        json_data = json.load(json_data_file)
        json_data_file.close()
        
        flat_list = []
        flat_cards = {}
        self.data = {}
        for k,v in json_data.iteritems():
            self.data[clean_unicode(v["name"])] = Edition(v)
            for stuff in v["cards"]:
                flat_list.append(clean_unicode(stuff["name"]))
                flat_cards[clean_unicode(stuff["name"])] = Card(stuff)
        self.flatList = sorted(list(set(flat_list)))
        self.flatCards = flat_cards

    #prints Set names and releaseDates
    def __str__(self):
        d = {}
        for k,v in self.data.iteritems():
            d[clean_unicode(v.name)] = v.releaseDate
        sorted_d = sorted(d, key=lambda key: d[key])
        
        result = ""
        for item in sorted_d:
            result += item + " " + d[item] + '\n'
        return result

    #When called this method will ask for user input, if Card is found then its information will be printed, otherwise it will tell you to try again
    def findCard(self, search):
        return self.flatCards.get(search)
    