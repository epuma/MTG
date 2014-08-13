from Magic import Magic
import json
import io

class Collection():

	def __init__(self):
		self.data = None

	def __str__(self):
		result = ""
		total = 0
		for k,v in self.data.iteritems():
			result += '\n' + k + '\n'
			for key, value in v.iteritems():
				result += key + ': ' + str(value) + '\n'
				total += value
		result += 'Total Number of Cards: ' + str(total)
		return result

	def load(self, fileName):
		json_data_file = open(fileName)
		json_data = json.load(json_data_file)
		json_data_file.close()

		self.data = json_data

	def save(self, fileName):
		with open(fileName, 'w') as outfile:
			json.dump(self.data, outfile)

	def newCollection(self, magic_obj, fileName = 'untitledCollection.json'):
		b = {}
		for sets in magic_obj.data.keys():
			b[sets] = {}
			for k,v in magic_obj.data[sets].data.iteritems():
				b[sets].update({k:0})

		with open(fileName, 'w') as outfile:
			json.dump(b, outfile)

	def updateCollection(self, magic_obj):
		for sets in magic_obj.data.keys():
			if sets not in self.data.keys():
				self.data[sets] = {}
				for k,v in magic_obj.data[sets].data.iteritems():
					self.data[sets].update({k:0})

	def addCard(self, edition, card, quantity):
		self.data[edition][card] += quantity

	def removeCard(self, edition, card, quantity):
		self.data[edition][card] -= quantity

	def getQuantity(self, edition, card):
		return self.data[edition][card]
