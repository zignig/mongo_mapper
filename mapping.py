#!/usr/bin/python 

import web,os
import redis,json,time
import requests,string

webdb = redis.Redis('localhost',db=2)
web.config.debug =True 
web_ttl = 2 

urls = (
	'/','index',
	'/box/(.*)','box',
	'/marker/(.*)','marker',
	'/(.+)','base'

)

points = {}
render = web.template.render('templates')
app = web.application(urls,globals())
server = "http://otile1.mqcdn.com/tiles/1.0.0/osm/"
#server = "http://bl3dr.com:8080/"

class index:
	def GET(self):
		return render.base()

class box:
	def GET(self,name):
		tmp  = web.input().keys()
		print tmp
		return ''

class marker:
	def GET(self,name):
		tmp  = web.input()
		points[(tmp['lat'],tmp['lng'])] = ''
		print points 
		return ''

tile_prefix = "tile:"
class base:
	def GET(self,name):
		if webdb.exists(tile_prefix+name):
			return webdb.get(tile_prefix+name)
		else:
			req = requests.get(server+name)	
			webdb.set(tile_prefix+name,req.content)
			return str(req.content)

if __name__ == "__main__":
	app.run()
