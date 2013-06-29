#!/usr/bin/python 

import web,os
import redis,json,time
import requests,string,traceback

webdb = redis.Redis('localhost',db=3)
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

class hackspaces:
	namespace = 'hackspace'
	def __init__(self):
		self.pages = []
		if webdb.exists(self.namespace):
			# process 
			self.data = json.loads(webdb.get(self.namespace))
			print('loaded '+str(len(self.data)))
		else:
			self.load_data()

	def load_page(self,tmp_dict,page):
		url = "http://hackspaces.org/wiki/Special:Ask/-5B-5BCategory:Hackspace-5D-5D/-3FWebsite/-3FLocation/mainlabel%3DHackspace/order%3DASC/limit%3D100/format%3Djson"
		
		print('fetch hackspace page '+str(page))
		try:
			if page > 0:
				r = requests.get(url+'/offset%3D'+str(page*100))
			else:
				r = requests.get(url)
			data = json.loads(r.text) 
			print data
			self.pages.append(r.text)
			print 'count '+str(len(data['items']))
			for i in data['items']:
				tmp_dict[i['label']] = i
			return tmp_dict
		except:
			print('fail on page '+str(page))
			return tmp_dict
		

	def load_data(self):
		print(' updating '+self.namespace)
		tmp_dict = {}
		self.items = []
		for i in range(0,15):
			tmp_dict = self.load_page(tmp_dict,i)
		for j in tmp_dict.keys():
			i = tmp_dict[j]
			if 'location' in i.keys():
				tmp = {'name':i['label']}
				tmp['lat'] = i['location']['lat']
				tmp['lon'] = i['location']['lon']
				if 'website' in i.keys():
					tmp['details'] = '<a target=new href="'+i['website']+'">'+i['website']+'</a>'
				self.items.append(tmp)
		webdb.set(self.namespace,json.dumps(self.items,indent=True))
		self.data = self.items
	
	
	def in_box(self,rect):
		print rect 
		items = [] 
		for i in self.data:
			if (i['lat'] > rect[1]) and (i['lat'] < rect[3]):
				if (i['lon'] > rect[0]) and (i['lon'] < rect[2]):
					items.append(i)
		return items

	def __repr__(self):
		return self.req 

class index:
	def GET(self):
		return render.base()

class box:
	def GET(self,name):
		tmp  = web.input()
		box = string.split(tmp['rect'],',')
		rect = []
		for i in box:
			x = float(i)
			rect.append(x)	
		items = hs.in_box(rect)
		web.header('Content-type', 'application/json') 
		return json.dumps(items)

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

global hs
hs = hackspaces()
if __name__ == "__main__":
	#hs.load_data()
	app.run()
