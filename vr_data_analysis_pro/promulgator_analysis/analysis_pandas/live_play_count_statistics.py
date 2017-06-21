#!/usr/local/bin/python
#-*- coding:utf8 -*-

import pandas as pd

import sys
sys.path.append('../../../')
import sql_Module.connectMysql as conMysql

sys.path.append('../../')

from sql_Module.mysql_const import const
from util import sql_tool
from live_play_entity import LivePlayEntity

from play_statistics_base import PlayStatisticsBase



class LivePlayStatistics(object):
	"""docstring for LivePlayStatistics"""
	# def __init__(self):
	# 	super(LivePlayStatistics, self).__init__()
	def __init__(self):
		super(LivePlayStatistics, self).__init__()
		self.conms = conMysql.ConnectMysql()
		self.conms.configMdb()

		self.loop = True
		self.chunkSize = 10000
		
	def installChunks(self, columns, kwargs):
		columnStr = ''
		for column in columns:
			columnStr += (column+',')
		columnStr = columnStr[0:len(columnStr)-1]
		self.whereSql = sql_tool.installFactors(kwargs)
		sql = 'SELECT '\
			  +columnStr\
			  +' from '\
			  +const.TABLE_NAME\
			  +self.whereSql
		print sql
		chunks = pd.read_sql(sql,\
	 			 con=self.conms.connector(), chunksize=self.chunkSize)
		return chunks
	def videoPlayCountDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_USERID]
		chunks = self.installChunks(columns, kwargs)
		df = pd.concat(chunks, ignore_index=False)
		# print type(df)
		groupbyVideoSid = df.groupby(const.COLUMN_VIDEOSID)
		print groupbyVideoSid.size()
		dfVideoSid = groupbyVideoSid.size().sort_values(ascending=False).to_frame()
		return dfVideoSid
	def videoPlayUserCountDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_USERID]
		chunks = self.installChunks(columns, kwargs)
		df = pd.concat(chunks, ignore_index=False)
		groupbyuserId = df.groupby([const.COLUMN_VIDEOSID,const.COLUMN_USERID])
		gr = groupbyuserId.size().to_frame()
		r = gr.groupby(const.COLUMN_VIDEOSID)
		dfUserId = r.size().to_frame()
		dfUserId.rename(columns={0: 'userCount'}, inplace=True)
		print dfUserId
		return dfUserId

	def videoInfoDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_VIDEONAME]
		chunksInfo = self.installChunks(columns,kwargs)
		dfInfo = pd.concat(chunksInfo, ignore_index=False)
		print dfInfo
		return dfInfo

	def mergeVideoPlayCountAndPlayUserCount(self,kwargs):
		df_videoPlayCount = self.videoPlayCountDataFrame(kwargs)
		df_videoPlayUserCount = self.videoPlayUserCountDataFrame(kwargs)
		dfMerge = pd.merge(df_videoPlayCount,df_videoPlayUserCount,left_index=True,right_index=True,how='left')
		print dfMerge
		return dfMerge

	def installVideoInfo(self,dfMerge,kwargs):
		df_videoInfo = self.videoInfoDataFrame(kwargs)

		dfMergeWithInfo = pd.merge(dfMerge,df_videoInfo,left_index=True,right_on=const.COLUMN_VIDEOSID,how='left').drop_duplicates()
		dfMergeWithInfo.rename(columns={0: 'playCount'}, inplace=True)
		dfMergeWithInfo = dfMergeWithInfo.reset_index()
		print dfMergeWithInfo
		return dfMergeWithInfo

	def to_excel(self,originDataFrame):
		from datetime import datetime
		# dt = datetime.now()
		# 获取日期：
		# today =datetime.date.today()    #获取今天日期
		# deltadays =datetime.timedelta(days=1)    #确定日期差额，如前天 days=2
		# yesterday =today -deltadays    # 获取差额日期，昨天
		# tomorrow =today +dletadays     # 获取差额日期，明天
		# # 格式化输出
		# ISOFORMAT='%Y%m%d%h%s' #设置输出格式
		# print today.strftime(ISOFORMAT)
		fileName = 'play_statistics'+'.xlsx'
		writer = pd.ExcelWriter(fileName)
		originDataFrame.to_excel(writer,'Sheet1')
		writer.save()
		return fileName
	def paserParams(self,kwargs):
		if kwargs.has_key(const.COLUMN_SCREENTYPE):

			if kwargs.has_key(const.COLUMN_VIDEOTYPE):
				videoType = kwargs[const.COLUMN_VIDEOTYPE]
				if videoType=='live':
					kwargs[const.COLUMN_SCREENTYPE]='1'
				
	def live_play_totalCount(self, **kwargs):
		self.paserParams(kwargs)
		df_merge = self.mergeVideoPlayCountAndPlayUserCount(kwargs)
		df_videoInfo = self.videoInfoDataFrame(kwargs)
		dfMergeWithInfo = self.installVideoInfo(df_merge,kwargs)
		
		print dfMergeWithInfo
		fileName = self.to_excel(dfMergeWithInfo)
		return fileName

if __name__ == '__main__':
	obj = LivePlayStatistics()
	obj.live_play_totalCount(startDate='2016-05-01',endDate='2017-05-03',videoType='VR',actionType='startplay',screenType='2',ascending=False)



