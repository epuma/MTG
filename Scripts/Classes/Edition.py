from Card import Card
from lib import clean_unicode

class Edition(object):
    #This is a class that will create an Edition Object. It sets all of the information as attributes and sets every card in the Edition to be a Card Object.
    
    def __init__(self, data):
        self.data = {}
        for k,v in data.iteritems():
            if k != "cards":
                setattr(self, k, v)
        for item in data["cards"]:
            self.data[clean_unicode(item["name"])] = Card(item)

    def getCard(self, name):
        return self.data[name]