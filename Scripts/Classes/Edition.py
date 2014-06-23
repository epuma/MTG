from Card import Card

class Edition(dict):
    #This is a class that will create an Edition Object. It sets all of the information as attributes and sets every card in the Edition to be a Card Object.
    
    def __init__(self, dict):
        for k,v in dict.iteritems():
            if k != "cards":
                setattr(self, k, v)
        for item in dict["cards"]:
            self[item["name"]] = Card(item)