#!/usr/bin/python -i 

import rlcompleter,readline 
readline.parse_and_bind('tab:complete')

from pymongo import MongoClient

client = MongoClient()
db = client.osm_store
tiles  = db.tiles

coll = db.collection_names()
print coll
