#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import fileinput


class ConnectMysql(object):
	"""docstring for connectMysql"""
	schema_name = 'vr_bi_table_video_play_statistics'
	table_name = 'video_play_statistics'
	select_rule = 'and'
	def __init__(self):
		super(ConnectMysql, self).__init__()
		return
	def configMdb(self):
		self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456abc', db=self.schema_name)
		self.cursor = self.conn.cursor()	
		return

	def getColumns(self):
		sql = "SELECT column_name FROM information_schema.columns WHERE table_schema ='%s' AND table_name='%s'" % (self.schema_name,self.table_name)
		self.cursor.execute(sql)
		r = self.cursor.fetchall()
		return r
	def installSubSqls(self,params):#key,value list
		subSqls = []
		for key in params.keys():
			value = params.get(key,'')
			subSql = ''
			if key=='id':
				subSql = " %s = %d " %(key, int(value))
			else:
				subSql = " %s = '%s' " %(key, value)
			subSqls.append(subSql)
			print subSql
		sql = "select * from video_play_statistics where"#'86203303158658702:00:00:00:00:00'
		for subSql in subSqls:
			sql = sql + subSql + self.select_rule
			
		sql = sql[0:len(sql)-len(self.select_rule)]
		print 'sql:'+sql
		return sql
	def select(self,sql):#list
		print 'sql:'+sql
		self.cursor.execute(sql)
		r = self.cursor.fetchall()
		print '获取到'+str(len(r))+'条纪录'
		return r
	def selectWithFactor(self,factor):
		sql = "select * from video_play_statistics where\
		%s" %(factor)
		r = self.select(sql)
		return 	r
	def selectFromId(self,startId,endId):
		sql = "select * from video_play_statistics where\
		id >= %d and id <= %d" %(startId, endId)
		r = self.select(sql)
		return 	r
	def totalCount(self, factor):
		sql = "select count(1) from video_play_statistics \
		%s" %(factor)
		r = self.select(sql)
		tuple = r[0]
		print '共有'+str(tuple[0])+'条纪录'
		return tuple[0]
	def searchFromMdb(self,params):
		subSqls = self.installSubSqls(params)
		self.select(subSqls)
		return
	def prepareSql(self,line):
		print '搜索...'
		params = line.split(' ')
		print 'params:'+str(params)
		self.select_rule = params.pop()
		if len(params) % 2 !=0:
			print '参数必须为key:value 使用空格分隔符 末尾制定‘and’ 或者‘or’规则'
			return 0
		paramsDic = {}
		for i in xrange(0,len(params),2):
			print 'i:'+str(i)
			key = params[i]
			value = params[i+1]
			paramsDic[key] = value
		self.searchFromMdb(paramsDic)
		return 1
	def handleInput(self,line):
		line = line.strip()
		if line == 'q':
			print '已退出'
			return 0
		else:
			if line == 'help':
				print '输入mysql的查询条件，以空格作为分隔符 末尾制定‘and’ 或者‘or’规则'
				return 1
			else:
				self.prepareSql(line)
	def waitingInput(self):
		for line in fileinput.input():
			if self.handleInput(line) ==0 :
				break
		return
	def close(self):
		self.conn.close()
		print 'db close'
		return
	def main(self):
		self.configMdb()
		self.waitingInput()
		return

def test():
	connectMysql = ConnectMysql()
	connectMysql.main()
# test()
