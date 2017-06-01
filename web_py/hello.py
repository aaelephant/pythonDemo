#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import web
web.config.debug = True
render = web.template.render('templates/')
db = web.database(dbn='mysql', user='root', pw='123456abc', db='test_todo')
urls = (
    '/', 'index',
    '/add', 'add'
)
class index:
	def GET(self):
	    todos = db.select('todo')
	    print 'get'
	    return render.hello(todos)
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
        n = db.insert('todo', title=i.title)
        print 'save success:'+i.title
        raise web.seeother('/')
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

