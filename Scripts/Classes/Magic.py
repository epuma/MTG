from Edition import Edition

class Magic(dict):
    #This is a class that will create a Magic object give the json database. It is a dictionary where the Key is the Code of the Edition and the Value is an Edition object. 
    
    def __init__(self, dict):
        for k,v in dict.iteritems():
            self[k] = Edition(v)