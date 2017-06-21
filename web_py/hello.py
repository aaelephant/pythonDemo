#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import web
import os
web.config.debug = True
curdir = os.path.abspath(os.path.dirname(__file__))
templates = curdir + '/templates/'
render = web.template.render(templates)
db = web.database(dbn='mysql', user='root', pw='123456abc', db='test_todo')
urls = (
    '/', 'index',
    '/add', 'add'
)
class index:
	def GET(self):
	    todos = db.select('todo')
	    print 'get'
	    return render.hello()
# class index:
# 	def GET(self, name):
# 		i = web.input(name=None)

# 		return render.hello(i.name)
		# return render.index(name)
    # def GET(self):
    #     return "Hello, world!"
class add:
    def POST(self):
    	print 'post'
        i = web.input()
        start_date = i.start_date
        end_date = i.end_date
        print '开始时间：'+str(start_date)
        print '截止时间：'+ str(end_date)
        # n = db.insert('todo', title=i.start_date)
        raise web.seeother('/')
if __name__ == "__main__":
    app = web.application(urls, globals())

    web.httpserver.runsimple(app.wsgifunc(),('127.0.0.1', 8088))
    app.run()

