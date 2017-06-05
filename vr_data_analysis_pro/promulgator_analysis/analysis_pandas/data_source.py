#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../../../')

from sql_Module import connectMysql as conMysql
from sql_Module.mysql_const import const

const.FACTOR_STARTDATE = 'startDate'
const.FACTOR_ENDDATE = 'endDate'

class DataSource(object):
	"""docstring for DataSource"""
	def __init__(self):
		super(DataSource, self).__init__()
		self.conms = conMysql.ConnectMysql()
		self.conms.configMdb()
		return
	def installFactors(self,factors):
		videoSid = ''
		startDate = ''
		endDate = ''
		actionType = ''
		log_tag = 'has_key:'
		if factors.has_key(const.COLUMN_VIDEOSID):
			print log_tag+const.COLUMN_VIDEOSID
			videoSid = factors[const.COLUMN_VIDEOSID]
		if factors.has_key(const.FACTOR_STARTDATE):
			print log_tag+const.FACTOR_STARTDATE
			startDate = factors[const.FACTOR_STARTDATE]
		if factors.has_key(const.FACTOR_ENDDATE):
			print log_tag+const.FACTOR_ENDDATE
			endDate = factors[const.FACTOR_ENDDATE]
		if factors.has_key(const.COLUMN_ACTIONTYPE):
			print log_tag+const.COLUMN_ACTIONTYPE
			actionType = factors[const.COLUMN_ACTIONTYPE]
		# tableName = const.TABLE_NAME

		sqls = []
		sql = ''
		
		if len(videoSid)>0:
			factor1 = const.COLUMN_VIDEOSID + const.EQUAL +'\'%s\'' % (videoSid)
			sqls.append(factor1)
		if len(startDate):
			factor2 = const.COLUMN_DATE + const.MORE_EQUAL + '\'%s\'' % (endDate)
			sqls.append(factor2)
		if len(endDate):
			factor3 =  const.COLUMN_DATE + const.LESS_EQUAL + '\'%s\'' % (endDate)
			sqls.append(factor3)
		if len(actionType):
			factor4 = const.COLUMN_ACTIONTYPE+const.EQUAL + '\'%s\'' % (actionType)
		for factor in sqls:
			sql += (factor + const.AND)
		if len(sql):
			sql = 'where ' + sql[0:len(sql)-len(const.AND)]
		return sql

	def sumEntry(self, factors):
		sql = self.installFactors(factors)
		count = self.conms.totalCount(sql)
		return count
	def loadData(self, callBack, *columns, **factors):
		print columns
		print factors
		totalCount = self.sumEntry(factors)

		totalPageNum = totalCount/const.PAGE_SIZE
		for pageNum in xrange(0,totalPageNum+1):
			self.execLoadData(columns, factors, pageNum, const.PAGE_SIZE, callBack)
	def execLoadData(self, columns, factors, pageNum, pageSize, callBack):
		
		columnSql = ''
		for column in columns:
			columnSql += (column+',')
		if len(columnSql):
			columnSql = columnSql[0:len(columnSql)-len(',')]
		else:
			columnSql = ' * '
		factorSql = self.installFactors(factors)
		sql = 'select ' \
		+ columnSql +\
		' from ' \
		+ const.TABLE_NAME +\
		' ' \
		+ factorSql +\
		' LIMIT ' \
		+ str(pageNum*pageSize) +\
		','\
		+ str(pageSize)
		r = self.conms.select(sql)
		callBack(r)
		# print r
		return

# data = DataSource().loadData(const.COLUMN_VIDEOSID,videoSid = 'tvn8opw0c3pq')
		