import os
from os import listdir
import io
import json
from distutils.version import StrictVersion
from PIL import Image, ImageTk
import urllib2


"""This only works for Python Version 2.7 for now.
	This checks the version and if its newer then downloads the file and displays changes since the previous version"""

def is_internet_on():
    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=10)
        return True
    except urllib2.URLError as err: pass
    return False

############################# Download JSON FIles #####################################

stuff = listdir('./JSON Files')
versionURL = 'http://mtgjson.com/json/version.json'
setURL = 'http://mtgjson.com/json/AllSets-x.json'
changeURL = 'http://mtgjson.com/json/changelog.json'

def download_stuff(name, location):
	try:
		r = urllib2.urlopen(location)
		content = r.read()
		e = open(name, 'wb')
		e.write(content)
		e.close
		print "Download of %s Completed!" %(name)
	except urllib2.URLError:
		print "Could not download %s. Please check your internet connection." %(name)

def save_json_data(json_file):
	json_data = open(json_file)
	data = json.load(json_data)
	json_data.close()
	return data

def show_changes(version):
	changeList = []
	changes = save_json_data('JSON Files/changelog.json')
	for items in changes:
		if StrictVersion(items["version"]) > StrictVersion(version):
			changeList.extend(items["changes"])
	return changeList

def download_json():
	if 'version.json' not in stuff:
		print "You did not have a version file. Downloading now..."
		download_stuff('JSON Files/version.json', versionURL)
	if 'AllSets-x.json' not in stuff:
		print "You did not have the MTG JSON file. Downloading now..."
		download_stuff('JSON Files/AllSets-x.json', setURL)
	if 'changelog.json' not in stuff:
		print "You did not have the changelog file. Downloading now..."
		download_stuff('JSON Files/changelog.json', changeURL)

	#Find Current Version
	currentVersion = open('JSON Files/version.json').read()[1: -1]

	#Check version from online
	s = urllib2.urlopen(versionURL)
	content = s.read()
	s.close()
	newVersion = content[1: -1]


	#Compares the version you have with the one online
	if StrictVersion(newVersion) > StrictVersion(currentVersion):
		#Update Version
		download_stuff('JSON Files/version.json', versionURL)
		#Update Set
		download_stuff('JSON Files/AllSets-x.json', setURL)
		#Update ChangeLog
		download_stuff('JSON Files/changelog.json', changeURL)
		print "Congratulations! You have downloaded the Latest Version"
		print "Changes since last version: "
		for items in show_changes(currentVersion):
			print items
	else:
		print "You already have the Newest Version"

######################### Download Image ##############################

def get_image(edition, name, wt, ht):
	try:
		url = 'http://mtgimage.com/setname/' + edition + '/' + name + '.jpg'
		print url
		image_bytes = urllib2.urlopen(url).read()
		data_stream = io.BytesIO(image_bytes)
		pil_image = Image.open(data_stream)

		if pil_image.format != 'JPEG':
			pil_image.save('temp_image.jpg', "JPEG")
			pil_image = Image.open('temp_image.jpg')
		
		w,h = pil_image.size
		pil_image = pil_image.resize((wt, ht), Image.ANTIALIAS)
		tk_image = ImageTk.PhotoImage(pil_image)
	except:
		tk_image = None
	return tk_image



