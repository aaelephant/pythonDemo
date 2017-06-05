#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import pandas as pd
from openpyxl import Workbook

import sys
sys.path.append('../../../')

import sql_Module.connectMysql as conMysql
from sql_Module.mysql_const import const

class PlayStatisticsBase(object):
	"""docstring for PlayStatisticsBase"""
	const.PLAY_COUNT = 'play_count'
	const.PLAY_USER_COUNT = 'user_count'
	def __init__(self):
		super(PlayStatisticsBase, self).__init__()
		self.conms = conMysql.ConnectMysql()
		self.conms.configMdb()

		self.loop = True
		self.chunkSize = 10000
	def writetoNewExcle(self, list, fileName):
		wb = Workbook()
		ws = wb.active
		ws.append([const.COLUMN_VIDEONAME,const.COLUMN_VIDEOSID,const.COLUMN_DATE,\
				   const.PLAY_COUNT,const.COLUMN_VIDEOTAGS,const.PLAY_USER_COUNT])
		totalNum = len(list)
		for row in xrange(2, totalNum+2):
			item = list[row-2]
			for column in xrange(1, len(item)+1):
				value = item[column-1]
				# if value is None:
					# value = ''
				ws.cell(column=column, row=row, value=value)	
			
			# col = list[index][1]
			# ws.cell(column=2, row=row, value=col)

		wb.save(fileName+'.xlsx')
		self.conms.close()
		return
	def getUserCount(self, videoSid):
		sql = 'SELECT '\
				  +const.COLUMN_USERID\
				  +' from '\
				  +const.TABLE_NAME\
				  +self.whereSql\
				  +' and '\
				  +const.COLUMN_VIDEOSID\
				  +const.EQUAL\
				  +" '"+videoSid+"' "
		print sql
		chunks = pd.read_sql(sql,\
	 			 con=self.conms.connector(), chunksize=self.chunkSize)
		df = pd.concat(chunks, ignore_index=False)
		r = df.groupby(const.COLUMN_USERID).size()
		count = len(r)
		print count
		return count
	def searchItemInfo(self, videoSid, playCount):
		sql = 'SELECT '\
				  +const.COLUMN_VIDEONAME\
				  +','\
				  +const.COLUMN_DATE\
				  +','\
				  +const.COLUMN_VIDEOTAGS\
				  +' from '\
				  +const.TABLE_NAME\
				  +self.whereSql\
				  +' and '\
				  +const.COLUMN_VIDEOSID\
				  +const.EQUAL\
				  +" '"+videoSid+"' "\
				  +' LIMIT 1'
		dataTuples = self.conms.select(sql)
		line = []
		if len(dataTuples):
		   line = dataTuples[0] 
		video = [line[0], videoSid, line[1],\
				playCount, line[2]
				]
		return video
	
	def installInfo(self, r):
		print len(r)
		num = 0
		dataList = []
		for index in r.index.values:
			video = self.searchItemInfo(index, r.at[index])
			userCount = self.getUserCount(index)
			video.append(userCount)
			dataList.append(video)
			num += 1
			if num>10:
				break
		return dataList