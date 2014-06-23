import os
import urllib2
from os import listdir
from distutils.version import StrictVersion

"""This only works for Python Version 2.7 for now.
This checks the version and if its newer then downloads the file"""

stuff = listdir('.')
versionURL = 'http://mtgjson.com/json/version.json'
setURL = 'http://mtgjson.com/json/AllSets-x.json'

def downloadStuff(name, location):
    r = urllib2.urlopen(location)
    content = r.read()
    e = open(name, 'wb')
    e.write(content)
    e.close

if 'version.json' not in stuff:
    downloadStuff('version.json', versionURL)
    print('You do not have a version file')
elif 'AllSets-x.json' not in stuff:
    downloadStuff('AllSets-x.json', setURL)
else:
    currentVersion = open('version.json').read()[1: -1]
    s = urllib2.urlopen(versionURL)
    content = s.read()
    newVersion = content[1: -1]
    s.close()
    if StrictVersion(newVersion) > StrictVersion(currentVersion):
        "Update Version"
        downloadStuff('version.json', versionURL)
        "Update Set"
        downloadStuff('AllSets-x.json', setURL)
        print('Congratulations! You have downloaded the Latest Version')
    else:
        print('You already have the Newest Version')


