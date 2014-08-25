from Magic import Magic
import json
import io
import datetime

class Collection():

	def __init__(self):
		self.data = None

	def __str__(self):
		result = ""
		total = 0
		for k,v in self.data.iteritems():
			result += '\n' + k + '\n'
			for key, value in v.iteritems():
				result += key + ': ' + str(value['quantity']) + '\n'
				total += value['quantity']
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
				b[sets].update({k: {'quantity' : 0, 'price' : ['N/A', 'N/A', 'N/A'], 'last_date' : '', 'notes' : ''}})

		with open(fileName, 'w') as outfile:
			json.dump(b, outfile)

	def updateCollection(self, magic_obj):
		for sets in magic_obj.data.keys():
			if sets not in self.data.keys():
				self.data[sets] = {}
				for k,v in magic_obj.data[sets].data.iteritems():
					self.data[sets].update({k: {'quantity' : 0, 'price' : ['N/A', 'N/A', 'N/A'], 'last_date' : '', 'notes' : ''}})

	def addCard(self, edition, card, quantity):
		self.data[edition][card]['quantity'] += quantity

	def removeCard(self, edition, card, quantity):
		self.data[edition][card]['quantity'] -= quantity

	def getQuantity(self, edition, card):
		return self.data[edition][card]['quantity']
	
	def getPrice(self, edition, card):
		return self.data[edition][card]['price']
	
	def getDateUpdated(self, edition, card):
		return self.data[edition][card]['last_date']
	
	def getNotes(self, edition, card):
		return self.data[edition][card]['notes']

	def updatePrice(self, edition, card, price):
		self.data[edition][card]['price'] = price
		self.data[edition][card]['last_date'] = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")

	def updateNotes(self, edition, card, notes):
		self.data[edition][card]['notes'] = notes

	def getTotalQuantity(self):
		total = 0
		for k,v in self.data.iteritems():
			for key, value in v.iteritems():
				total += value['quantity']
		return total

	def getTotalPrice(self):
		total_price = [0,0,0]
		for k,v in self.data.iteritems():
			for key, value in v.iteritems():
				for n in [0, 1, 2]:
					if value['price'][n] == 'N/A':
						total_price[n] += 0
					else:
						total_price[n] += float(value['price'][n])
		return total_price






