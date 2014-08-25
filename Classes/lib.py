REPLACEMENTS = {
	u'\u2014' : '-',
	u'\u2E3A' : '-',
	u'\u2212' : '-',
	u'\xc6' : 'AE',
	u'\xe9' : 'e',
	u'\xe0' : 'a',
	u'\xfa' : 'u',
	u'\xe2' : 'a',
	u'\xfb' : 'u',
	u'\xe1' : 'a',
	u'\xed' : 'i',
	u'\xae' : 'R',
	u'\xf6' : 'o',
	u'\u00FC' : 'u',
	u'\u2019' : "'"
}

def clean_unicode(item):
	new_item = None
	if isinstance(item, list):
		new_item = []
		for things in item:
			new_things = None
			if isinstance(things, dict):
				new_things = {}
				for k,v in things.iteritems():
					new_things[clean_unicode(k)] = clean_unicode(v)
			else:
				new_things = clean_unicode(things)
			new_item.append(new_things)
	elif isinstance(item, dict):
		new_things = {}
		for k,v in item.iteritems():
			new_things[clean_unicode(k)] = clean_unicode(v)
		new_item = new_things
	elif isinstance(item, basestring):
		new_item = ''
		for s, r in REPLACEMENTS.iteritems():
			item = item.replace(s, r)
		new_item = item.encode('ascii', 'replace')
	else:
		new_item = item
	return new_item