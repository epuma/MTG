import os
import urllib2
import json
from os import listdir
from distutils.version import StrictVersion

"""This only works for Python Version 2.7 for now.
This checks the version and if its newer then downloads the file and displays changes since the previous version"""

stuff = listdir('.')
versionURL = 'http://mtgjson.com/json/version.json'
setURL = 'http://mtgjson.com/json/AllSets-x.json'
changeURL = 'http://mtgjson.com/json/changelog.json'

def downloadStuff(name, location):
	try:
		r = urllib2.urlopen(location)
		content = r.read()
		e = open(name, 'wb')
		e.write(content)
		e.close
		print "Download Completed!"
	except urllib2.URLError:
		print "Could not download %s. Please check your internet connection." %(name)

def jsonSave(json_file):
	json_data = open(json_file)
	data = json.load(json_data)
	json_data.close()
	return data

def showChanges(version):
	changeList = []
	changes = jsonSave('changelog.json')
	for items in changes:
		if StrictVersion(items["version"]) > StrictVersion(version):
			changeList.extend(items["changes"])
	return changeList


if 'version.json' not in stuff:
	print "You did not have a version file. Downloading now..."
	downloadStuff('version.json', versionURL)
elif 'AllSets-x.json' not in stuff:
	print "You did not have the MTG JSON file. Downloading now..."
	downloadStuff('AllSets-x.json', setURL)
elif 'changelog.json' not in stuff:
	print "You did not have the changelog file. Downloading now..."
	downloadStuff('changelog.json', changeURL)
else:
	#Find Current Version
	currentVersion = open('version.json').read()[1: -1]

	#Check version from online
	try:
		s = urllib2.urlopen(versionURL)
		content = s.read()
		s.close()
		newVersion = content[1: -1]


		#Compares the version you have with the one online
		if StrictVersion(newVersion) > StrictVersion(currentVersion):
			#Update Version
			downloadStuff('version.json', versionURL)
			#Update Set
			downloadStuff('AllSets-x.json', setURL)
			#Update ChangeLog
			downloadStuff('changelog.json', changeURL)
			print "Congratulations! You have downloaded the Latest Version"
			print "Changes since last version: "
			for items in showChanges(currentVersion):
				print items
		else:
			print "You already have the Newest Version"
	except urllib2.URLError:
		print "Unable to Check status. Please check if you have Internet"


