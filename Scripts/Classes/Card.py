class Card(dict):
    #This is a class that will create a Card Object. All of the information of the Card is an attribute of the card
    
    def __init__(self, dict):
        for k,v in dict.iteritems():
            setattr(self, k, v)