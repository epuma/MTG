from lib import clean_unicode

class Card(object):
	#This is a class that will create a Card Object. All of the information of the Card is an attribute of the card
    
	def __init__(self, data):
		self.attrlist = []
		for k,v in data.iteritems():
			new_v = clean_unicode(v)
			setattr(self, k, new_v)
			self.attrlist.append(k)

	#This method is for displaying all the information of the card
	def __str__(self):
		result = ""
		for item in self.attrlist:
			result += item + ': ' + str(getattr(self, item)) + '\n'
		return result
