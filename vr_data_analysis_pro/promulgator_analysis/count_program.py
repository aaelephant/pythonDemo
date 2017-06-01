#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../../')

import sql_Module.connectMysql as conMysql
"""导入sql_Module文件夹下的模块"""
from collections import Counter
from openpyxl import Workbook
from openpyxl import load_workbook
import thread
# from openpyxl.compat import range
# from openpyxl.utils import get_column_letter


class CountProgram(object):
	"""docstring for CountProgram"""
	def __init__(self):
		super(CountProgram, self).__init__()
		self.conms = conMysql.ConnectMysql()
		self.conms.configMdb()
		return

	def readWithFactor(self, startDate, endDate, pageNum, pageSize):
		dataTuples = self.conms.selectWithFactor("date >= '%s' and date <= '%s' LIMIT %d, %d" %(startDate, endDate, pageNum*pageSize,pageSize))
		# print 'dataTuples:'+str(dataTuples[0])
		tuples = self.conms.getColumns()

		column_names = []
		for cur in tuples:
			# print 'column_name:'+cur[0]+'\n'
			column_names.append(cur[0])
		# dataDics = []
		videoList = []
		for dataTuple in dataTuples:
			itemDics = []
			for i in xrange(0,len(column_names)):
				# dataDic = {}
				# dataDic[column_names[i]] = dataTuple[i]
				# itemDics.append(dataDic)
				if column_names[i] == 'videoSid':
					videoList.append(dataTuple[i])
			# print 'itemDics:'+str(itemDics)+'\n'
			# dataDics.append(itemDics)
		r = Counter(videoList)
		print 'r:' + str(len(r.most_common()))
		# print 'videoList:'+str(len(videoList))+'条'
		return r
	def readPage(self, pageNum, pageSize):
		dataTuples = self.conms.selectFromId(pageNum*pageSize,(pageNum+1)*pageSize)
		# print 'dataTuples:'+str(dataTuples[0])
		tuples = self.conms.getColumns()

		column_names = []
		for cur in tuples:
			# print 'column_name:'+cur[0]+'\n'
			column_names.append(cur[0])
		# dataDics = []
		videoList = []
		for dataTuple in dataTuples:
			itemDics = []
			for i in xrange(0,len(column_names)):
				# dataDic = {}
				# dataDic[column_names[i]] = dataTuple[i]
				# itemDics.append(dataDic)
				if column_names[i] == 'videoSid':
					videoList.append(dataTuple[i])
			# print 'itemDics:'+str(itemDics)+'\n'
			# dataDics.append(itemDics)
		r = Counter(videoList)
		print 'r:' + str(len(r.most_common()))

		return r
	def continueWriteToExcle(self, path):
		wb = load_workbook(path)
		print wb.get_sheet_names() 
	def writetoNewExcle(self,list):
		wb = Workbook()
		ws = wb.active
		ws.append(['videoSid','value'])
		totalNum = len(list)
		for row in xrange(2, totalNum+2):
			index = row-2#totalNum+1-row#
			col = list[index][0]
			ws.cell(column=1, row=row, value=col)
			col = list[index][1]
			ws.cell(column=2, row=row, value=col)

		wb.save("videoSid.xlsx")
		self.conms.close()
	def totalCount(self, factor):
		r = self.conms.totalCount(factor)

		return r
	def countPlayVideo(self):
		startDate = '2016-12-15'
		endDate = '2016-12-15'
		tableName = self.conms.table_name
		# startDateSql = "SELECT COUNT( 1 ) FROM %s WHERE 'date' >= '%s' " %(tableName, startDate)
		# endDateSql = "SELECT COUNT( 1 ) FROM %s WHERE 'date' <= '%s' " %(tableName, endDate)
		# sql = "SELECT ( %s ) AS 'startDate', ( %s ) AS 'endDate'" %(startDateSql, endDateSql)
		sql = "where date >= '%s' and date <= '%s'" % (startDate, endDate)
		count = self.conms.totalCount(sql)
		# tuple = r[0]
		# print '共有'+str(tuple[0])+'条纪录'
		# count = tuple[0]
		pageSize = 1000
		totalPageNum = count/pageSize
		remainder = count%pageSize
		# list = []
		
		# for pageNum in xrange(0,totalPageNum):
		# 	preCounter = self.readWithFactor(startDate, endDate, pageNum, pageSize)	
		# 	list += preCounter
		# preCounter = self.readWithFactor(startDate, endDate, totalPageNum, pageSize)	
		# list += preCounter
		preCounter = self.readWithFactor(startDate, endDate, 0, pageSize)	
		for pageNum in xrange(1,totalPageNum):
			curCounter = self.readWithFactor(startDate, endDate, pageNum, pageSize)	
			preCounter.update(curCounter)  
		curCounter = self.readWithFactor(startDate, endDate, totalPageNum, pageSize)	
		preCounter.update(curCounter)
		list = preCounter.most_common()
		print 'list:'+str(len(list))
		self.writetoNewExcle(list)
		return
	def main(self):
		list = self.countPlayVideo()
		self.writetoNewExcle(list)
		return
cp = CountProgram()
# cp.continueWriteToExcle('continue.xlsx')
cp.countPlayVideo()