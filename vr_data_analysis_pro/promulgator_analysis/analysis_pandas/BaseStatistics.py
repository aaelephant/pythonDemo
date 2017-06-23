#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import os
import sys
import ijson
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

import MySQLdb

sys.path.append('../../')
from config import config

sys.path.append('../../../')
from sql_Module.mysql_const import const


class BaseStatistics(object):
	"""docstring for BaseStatistics"""
	def __init__(self, inputPath):
		super(BaseStatistics, self).__init__()
		self.inputPath = inputPath
	def to_sql(self, originDataFrame, eventSubType):
		dbType = config.configs['db']['dbType']
		host = config.configs['db']['host']
		port = config.configs['db']['port']
		user = config.configs['db']['user']
		passwd = config.configs['db']['password']
		database = config.configs['db']['database']
		charset = config.configs['db']['charset']
		echo = config.configs['db']['echo']
		cnx = create_engine('%s://%s:%s@%s:%d/%s?charset=%s'%(dbType,user,passwd,host,port,database,charset) ,echo=echo)
		# conn = MySQLdb.connect(host='localhost', user='root', passwd='123456abc', db='vr_bi_statistics')
		originDataFrame.to_sql(name=self.eventType+'_'+eventSubType+'_statistics',con=cnx,if_exists='replace',index=False)
	def filterItem(self, item, infoColumns , factors):
		log_tag = 'has_key:'
		if factors.has_key(const.COLUMN_VIDEOSID):
			# print log_tag+const.COLUMN_VIDEOSID
			if item.has_key(const.COLUMN_VIDEOSID):
				if item[const.COLUMN_VIDEOSID]!=factors[const.COLUMN_VIDEOSID]:
					return False
		if factors.has_key(const.FACTOR_STARTDATE):
			# print log_tag+const.FACTOR_STARTDATE
			if item.has_key(const.FACTOR_STARTDATE):
				if item[const.FACTOR_STARTDATE]<factors[const.FACTOR_STARTDATE]:
					return False
		if factors.has_key(const.FACTOR_ENDDATE):
			# print log_tag+const.FACTOR_ENDDATE
			if item.has_key(const.FACTOR_ENDDATE):
				if item[const.FACTOR_ENDDATE]>factors[const.FACTOR_ENDDATE]:
					return False
		if factors.has_key(const.COLUMN_ACTIONTYPE):
			# print log_tag+const.COLUMN_ACTIONTYPE
			if item.has_key(const.COLUMN_ACTIONTYPE):
				actionType = item[const.COLUMN_ACTIONTYPE]
				if actionType!=factors[const.COLUMN_ACTIONTYPE]:
					# print 'actionType'
					return False
		if factors.has_key(const.COLUMN_VIDEOTYPE):
			# print log_tag+const.COLUMN_VIDEOTYPE
			if item.has_key(const.COLUMN_VIDEOTYPE):
				if item[const.COLUMN_VIDEOTYPE]!=factors[const.COLUMN_VIDEOTYPE]:
					return False
		if factors.has_key(const.COLUMN_SCREENTYPE):
			# print log_tag+const.COLUMN_SCREENTYPE
			if item.has_key(const.COLUMN_SCREENTYPE):
				screenType = item[const.COLUMN_SCREENTYPE]
				if screenType!=factors[const.COLUMN_SCREENTYPE]:
					return False
		keys = item.keys()
		for key in keys:
			for column in infoColumns:
				if key == column:
					keys.remove(key)
		for key in keys:
			item.pop(key)
		# print item.keys()
		# print item
		return True
	def getAllDirs(self, folderPath):

		names = [name for name in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, name))]
		return names
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
	def installColumns(self):
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_VIDEOTAGS]
		return columns
	def videoInfoDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = self.installColumns()
		dfInfo = self.installDataFrames(columns,kwargs)
		# dfInfo = pd.concat(chunksInfo, ignore_index=False)
		# print dfInfo
		return dfInfo
	def installVideoInfo(self,dfMerge,kwargs):
		df_videoInfo = self.videoInfoDataFrame(kwargs)
		# print df_videoInfo
		dfMergeWithInfo = pd.merge(dfMerge,df_videoInfo,left_index=True,right_on=const.COLUMN_VIDEOSID,how='left').drop_duplicates()
		dfMergeWithInfo.rename(columns={0: 'playCount'}, inplace=True)
		dfMergeWithInfo = dfMergeWithInfo.reset_index()
		# print dfMergeWithInfo
		return dfMergeWithInfo
	def installItemJson(self, dirName, infoColumns, kwargs):
		path = os.path.join(self.inputPath,self.eventType,dirName,'log.vr.'+self.eventType+'.log')
		print path
		with open(path, 'r') as f:
		    objects = ijson.items(f, 'item')
		    columns = list(objects)
		curColumns = []
		for item in columns:
			filterR = self.filterItem(item,infoColumns,kwargs)
			if filterR == True:
				# print 'drop'
				curColumns.append(item)
				# columns.remove(item)
		jsonStr = json.dumps(curColumns)
		return jsonStr
	def installDataFrames(self, infoColumns, kwargs):
		
		dirNames = self.getAllDirs(os.path.join(self.inputPath,self.eventType))
		
		curDirNames = []
		if kwargs.has_key(const.FACTOR_STARTDATE):
			startDate = kwargs[const.FACTOR_STARTDATE]
			for dirName in dirNames:
	 			y = datetime.strptime(startDate, '%Y-%m-%d')
				z = datetime.strptime(dirName, '%Y%m%d')
				r = z>=y
	 			if r:
	 				curDirNames.append(dirName)
	 	else:
	 		curDirNames = dirNames
	 	
		df = pd.DataFrame()
	 	for dirName in curDirNames:
	 		jsonStr = self.installItemJson(dirName, infoColumns, kwargs)
	 		curDF = pd.read_json(jsonStr)
			df = df.append(curDF)
		return df
	
	def videoCountDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = self.installColumns()
		df = self.installDataFrames(columns, kwargs)
		# df = pd.concat(chunks, ignore_index=False)
		if pd.isnull(df).empty == True:
			raise Exception('所选条件内没有统计数据', 1)
		groupbyVideoSid = df.groupby(const.COLUMN_VIDEOSID)
		# print groupbyVideoSid.size()
		dfVideoSid = groupbyVideoSid.size().sort_values(ascending=False).to_frame()
		return dfVideoSid
	def paserParams(self,kwargs):
		print kwargs
		if kwargs.has_key(const.EVENT_TYPE):
			self.eventType = kwargs[const.EVENT_TYPE]
		else:
			raise Exception('must have eventType', 1)
	def save(self, resultDF, eventSubType):
		self.to_sql(resultDF, eventSubType)

	def start(self, **kwargs):
		self.paserParams(kwargs)
		