import urllib2

#This function gets prices from TCGPlayer and returns a list of High Medium and Low prices

REPLACEMENTS = {
	'Commander 2013 Edition' : 'Commander 2013',
	'Deckmasters' : 'Deckmasters Garfield vs. Finkel',
	'Eighth Edition' : '8th Edition',
	'Limited Edition Alpha' : 'Alpha Edition',
	'Limited Edition Beta' : 'Beta Edition',
	'Magic 2014 Core Set' : 'Magic 2014',
	'Magic 2015 Core Set' : 'Magic 2015',
	'Magic: The Gathering-Commander' : 'Commander',
	'Magic: The Gathering-Conspiracy' : 'Conspiracy',
	'Ninth Edition' : '9th Edition',
	'Planechase 2012 Edition' : 'Planechase 2012',
	'Ravnica: City of Guilds' : 'Ravnica',
	'Seventh Edition' : '7th Edition',
	'Tenth Edition' : '10th Edition',
	'Time Spiral "Timeshifted"' : 'Timeshifted',
	'Introductory Two-Player Set' : '',
	'Masters Edition' : '',
	'Masters Edition II' : '',
	'Masters Edition III' : '',
	'Masters Edition IV' : '',
	'Modern Event Deck 2014' : '',
	'Promo set for Gatherer' : '',
	'Rivals Quick Start Set' : '',
	'Vintage Masters' : ''
}

def retrieve_prices(card_name, edition):
	
	url = 'http://magic.tcgplayer.com/db/magic_single_card.asp?cn=' + card_name.replace(' ', '%20') + '&sn=' + edition.replace(' ', '%20')
	
	print url
	
	response = urllib2.urlopen(url)
	html_code = response.read()
	prices = []

	if (html_code.find('Price N/A') != -1) or html_code.find('<B>$') == -1:
		prices = ['N/A', 'N/A', 'N/A']
	else:
		html_code = html_code.split('<B>$')[1:]
		for items in html_code:
			price = items[0:items.find('</b>')]
			prices.append(price)
	return prices

def get_prices(card_name, edition):
	new_edition_name = ''
	for k, v in REPLACEMENTS.iteritems():
		edition = edition.replace(k, v)
	new_edition_name = edition
	prices = retrieve_prices(card_name, new_edition_name)
	if prices == ['N/A', 'N/A', 'N/A'] or prices == []:
		prices = retrieve_prices(card_name, '')
	return prices








