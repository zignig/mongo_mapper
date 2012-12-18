#!/usr/bin/python 

import web,os
import redis,json,time
import requests

webdb = redis.Redis('localhost',db=1)
web.config.debug =True 
web_ttl = 2 

urls = (
	'/','index',
	'/(.+)','base'
)
r = requests.session()
server = 'http://a.tile.openstreetmap.org/'
render = web.template.render('templates')
app = web.application(urls,globals())

class index:
	def GET(self):
		return render.base()

		
class ident:
	def GET(self,name):
		print name
		return json.dumps(cq.id(name),indent=4)

class base:
	def GET(self,name):
		if webdb.exists('complete:'+name):
			return webdb.get('complete:'+name)
		else:
			req = r.get(server+name)	
			print req.url
			webdb.set('complete:'+name,req.content)
			return str(req.content)

if __name__ == "__main__":
	app.run()
