#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import web
import os
# import sys
# sys.path.append('../../')

from promulgator_analysis import count_program as countP
from promulgator_analysis.analysis_pandas import live_play_count_statistics as countPlayStatistics

web.config.debug = True
curdir = os.path.abspath(os.path.dirname(__file__))
templates = curdir + '/web' + '/templates/'
render = web.template.render(templates)

db = web.database(dbn='mysql', user='root', pw='123456abc', db='test_todo')
urls = (
    '/', 'Index',
    '/startAnalysis', 'StartAnalysis',
    '/analysis_result', 'Analysis_result',
    '/download', 'Download'
)

fileName = 'd'

class Index:
	def GET(self):
	    # todos = db.select('todo')
	    print 'get'
	    return render.analysis()
# class index:
# 	def GET(self, name):
# 		i = web.input(name=None)

# 		return render.hello(i.name)
		# return render.index(name)
    # def GET(self):
    #     return "Hello, world!"
class StartAnalysis:

    def POST(self):
    	print 'post'
        i = web.input()
        start_date = i.start_date
        end_date = i.end_date
        videoType = i.videoType
        
        print '开始时间：'+str(start_date)
        print '截止时间：'+ str(end_date)
        print '视频类型: '+str(videoType)
        # n = db.insert('todo', title=i.start_date)
        file_name = self.analysis(start_date, end_date, videoType)
        fileName = file_name
        raise web.seeother('/analysis_result?start_date='+start_date+'&end_date='+end_date+'&file_name='+file_name+'&videoType='+videoType)
        # return render.analysis_result('result')
    def analysis(self, startDate, endDate, videoType):
        counter = countPlayStatistics.LivePlayStatistics()
        file_name = counter.live_play_totalCount(startDate=startDate,endDate=endDate,videoType=videoType,actionType='startplay',ascending=False)
        return file_name

class Analysis_result(object):
    """docstring for Analysis_result"""
    def GET(self):
        i = web.input()
        return render.analysis_result(start_date=i.start_date,end_date=i.end_date, file_name=i.file_name, videoType=i.videoType)
    # def __init__(self, arg):
        # super(Analysis_result, self).__init__()
        # self.arg = arg
BUF_SIZE = 262144
class Download:
    def POST(self):
        i = web.input()
        file_name = i.file_name;
        print 'file_name:' + str(file_name)
        file_path = os.path.join('promulgator_analysis/analysis_pandas', file_name)
        f = None
        try:
            f = open(file_path, "rb")
            web.header('Content-Type','application/octet-stream')
            web.header('Content-disposition', 'attachment; filename=%s' % file_name)
            while True:
                c = f.read(BUF_SIZE)
                if c:
                    yield c
                else:
                    break
        except Exception, e:
            print e
            yield 'Error'
        finally:
            if f:
                f.close()  
if __name__ == "__main__":
    app = web.application(urls, globals())

    web.httpserver.runsimple(app.wsgifunc())
    app.run()

