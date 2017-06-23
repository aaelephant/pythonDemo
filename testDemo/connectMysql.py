#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import fileinput


class ConnectMysql(object):
	"""docstring for connectMysql"""
	def __init__(self):
		super(ConnectMysql, self).__init__()
		return
	def configMdb(self):
		conn = MySQLdb.connect(host='localhost', user='root', passwd='123456abc', db='vr_bi_table_video_play_statistics')
		self.cursor = conn.cursor()	
		return
	def getColumns(self):
		sql = 'SELECT column_name, column_type FROM information_schema.columns WHERE table_schema=\'vr_bi_table_video_play_statistics\' AND table_name=\'video_play_statistics\''
		self.cursor.execute(sql)
		columns = self.cursor.fetchall()
		for column in columns:
			if column[1] == 'varchar(50)':
				print 'is varchar(50)\n'
			print 'column_name:'+column[0]+'\ncolumn_type:'+column[1];
		return
	def searchFromMdb(self,line):
		print '搜索...'
		params = line.split(' ')
		key = ''
		value = ''
		if len(params)==2:
			key = params[0]
			value = params[1]
		else:
			print '参数必须为两个'
			return
		print 'key:'+key+' value:'+value
		sql = "select * from video_play_statistics where %s = '%s'" % (key,value)#'86203303158658702:00:00:00:00:00'
		print 'sql:'+sql
		self.cursor.execute(sql)
		r = self.cursor.fetchall()
		print '共有'+str(len(r))+'条纪录'
		return
	def handleInput(self,line):
		line = line.strip()
		if line == 'q':
			print '已退出'
			return 0
		else:
			self.searchFromMdb(line)
			return 1
	def waitingInput(self):
		for line in fileinput.input():
			if self.handleInput(line) ==0 :
				break
		return
	def main(self):
		self.configMdb()
		self.getColumns()
		self.waitingInput()
		return

def test():
	connectMysql = ConnectMysql()
	connectMysql.main()
	
	
test()
