#!/usr/bin/python -i 

import rlcompleter,readline 
readline.parse_and_bind('tab:complete')

from pymongo import MongoClient

client = MongoClient()
db = client.osm_store
tiles  = db.tiles
markers = db.markers
for i in markers.find():
	print i
