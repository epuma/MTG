class Card(dict):
    #This is a class that will create a Card Object. All of the information of the Card is an attribute of the card
    
    def __init__(self, dict):
        self.attrlist = []
        for k,v in dict.iteritems():
            setattr(self, k, v)
            self.attrlist.append(k)

    def printCard(self):
        for item in self.attrlist:
            print item + ': ', getattr(self, item)
