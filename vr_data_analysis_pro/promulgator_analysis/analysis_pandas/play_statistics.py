#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import os
import sys
import ijson
import json
import pandas as pd
from datetime import datetime
sys.path.append('../../../')
# import sql_Module.connectMysql as conMysql
import MySQLdb

sys.path.append('../../')

from sql_Module.mysql_const import const
from util import sql_tool
from live_play_entity import LivePlayEntity

from play_statistics_base import PlayStatisticsBase
from sqlalchemy import create_engine
import matplotlib.pyplot as plt



class PlayStatistics(object):
	"""docstring for PlayStatistics"""
	# def __init__(self):
	# 	super(PlayStatistics, self).__init__()
	def __init__(self, inputPath):
		super(PlayStatistics, self).__init__()
		self.inputPath = inputPath
		# self.outPath = outPath
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
	def installItemJson(self, dirName, infoColumns, kwargs):
		path = os.path.join(self.inputPath,self.eventType,dirName,'log.vr.'+self.eventType+'.log')
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
	def installChunks(self, infoColumns, kwargs):
		
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
		df = pd.DataFrame()
	 	for dirName in curDirNames:
	 		jsonStr = self.installItemJson(dirName, infoColumns, kwargs)
	 		curDF = pd.read_json(jsonStr)
			df = df.append(curDF)

		# print df
		# chunks = pd.read_sql(sql,\
	 			 # con=self.conms.connector(), chunksize=self.chunkSize)
		return df
	def videoPlayCountDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_USERID]
		df = self.installChunks(columns, kwargs)
		# df = pd.concat(chunks, ignore_index=False)
		# print type(df)
		groupbyVideoSid = df.groupby(const.COLUMN_VIDEOSID)
		# print groupbyVideoSid.size()
		dfVideoSid = groupbyVideoSid.size().sort_values(ascending=False).to_frame()
		return dfVideoSid
	def videoPlayUserCountDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_USERID]
		df = self.installChunks(columns, kwargs)
		# df = pd.concat(chunks, ignore_index=False)
		groupbyuserId = df.groupby([const.COLUMN_VIDEOSID,const.COLUMN_USERID])
		gr = groupbyuserId.size().to_frame()
		r = gr.groupby(const.COLUMN_VIDEOSID)
		dfUserId = r.size().to_frame()
		dfUserId.rename(columns={0: 'userCount'}, inplace=True)
		# print dfUserId
		return dfUserId

	def videoInfoDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_VIDEONAME]
		dfInfo = self.installChunks(columns,kwargs)
		# dfInfo = pd.concat(chunksInfo, ignore_index=False)
		# print dfInfo
		return dfInfo

	def mergeVideoPlayCountAndPlayUserCount(self,kwargs):
		df_videoPlayCount = self.videoPlayCountDataFrame(kwargs)
		df_videoPlayUserCount = self.videoPlayUserCountDataFrame(kwargs)
		dfMerge = pd.merge(df_videoPlayCount,df_videoPlayUserCount,left_index=True,right_index=True,how='left')
		# print dfMerge
		return dfMerge

	def installVideoInfo(self,dfMerge,kwargs):
		df_videoInfo = self.videoInfoDataFrame(kwargs)
		# print df_videoInfo
		dfMergeWithInfo = pd.merge(dfMerge,df_videoInfo,left_index=True,right_on=const.COLUMN_VIDEOSID,how='left').drop_duplicates()
		dfMergeWithInfo.rename(columns={0: 'playCount'}, inplace=True)
		dfMergeWithInfo = dfMergeWithInfo.reset_index()
		# print dfMergeWithInfo
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
	def to_sql(self, originDataFrame, eventSubType):
		cnx = create_engine('mysql+pymysql://root:123456abc@localhost:3306/vr_bi_statistics?charset=utf8',echo=True)
		# conn = MySQLdb.connect(host='localhost', user='root', passwd='123456abc', db='vr_bi_statistics')
		originDataFrame.to_sql(name=self.eventType+'_'+eventSubType+'_statistics',con=cnx,if_exists='replace',index=False)

	def paserParams(self,kwargs):
		if kwargs.has_key(const.COLUMN_SCREENTYPE):

			if kwargs.has_key(const.COLUMN_VIDEOTYPE):
				videoType = kwargs[const.COLUMN_VIDEOTYPE]
				if videoType=='live':
					kwargs[const.COLUMN_SCREENTYPE]='1'
			
	def withplotly(self, dfMergeWithInfo):
		import plotly.plotly as py
		import pandas as pd
		from plotly.graph_objs import *
		import plotly 
		plotly.tools.set_credentials_file(username='qs88', api_key='15EhVCwBDqWBANW8zQ2A')
		data = Data([
		    Bar(
		        x=dfMergeWithInfo["videoSid"],
		        y=dfMergeWithInfo["playCount"]
		    )
		])
		layout = Layout(
		    title='2014 MN Capital Budget',
		    font=Font(
		        family='Raleway, sans-serif'
		    ),
		    showlegend=False,
		    xaxis=XAxis(
		        tickangle=-45
		    ),
		    bargap=0.05
		)
		fig = Figure(data=data, layout=layout)
		plot_url = py.plot(data,filename='MN Capital Budget - 2014')
		py.image.save_as(fig, 'mn-14-budget.png')	
	def withbokeh(self,dfMergeWithInfo):
		from bokeh.charts import Bar, output_file, show
		details = dfMergeWithInfo["videoSid"].values.tolist()

		amount = list(dfMergeWithInfo["playCount"].astype(float).values)
		print amount
		bar = Bar(dfMergeWithInfo, filename="bar.html")
		bar.title("MN Capital Budget - 2014").xlabel("Detail").ylabel("Amount")
		show(bar)
	def withplot(self,dfMergeWithInfo):
		layout = ('physics', 'chemistry', 1997, 2000)
		figsize = (20, 10)
		pl = dfMergeWithInfo.plot.barh(style=['bar'],logx=True,stacked=True,sort_columns=True,rot=30,layout=layout)#(kind='barh',yticks=dfMergeWithInfo['videoSid'])
		plt.show()#.save('play.png')
	def play_totalCount(self, **kwargs):
		print kwargs
		if kwargs.has_key(const.EVENT_TYPE):
			self.eventType = kwargs[const.EVENT_TYPE]
		else:
			print 'must have eventType'
			return
		eventSubType = ''
		if kwargs.has_key(const.EVENT_SUB_TYPE):
			eventType = kwargs[const.EVENT_SUB_TYPE]
		self.paserParams(kwargs)
		df_merge = self.mergeVideoPlayCountAndPlayUserCount(kwargs)
		# df_videoInfo = self.videoInfoDataFrame(kwargs)
		dfMergeWithInfo = self.installVideoInfo(df_merge,kwargs)
		# dfMergeWithInfo = dfMergeWithInfo.set_index(keys=const.COLUMN_VIDEOSID)
		
		self.to_sql(dfMergeWithInfo,eventType)
		# print dfMergeWithInfo
		# fileName = self.to_excel(dfMergeWithInfo)
		# return fileName

if __name__ == '__main__':
	eventTypeDetail = 'detail'
	eventTypeLive = 'live'
	obj = PlayStatistics('/Users/qbshen/Work/python/Demand/json_logs/output/datas/')
	# obj.installChunks(videoType='VR',a='a')
	# obj.play_totalCount(eventType=eventTypeLive,startDate='2017-06-16',actionType='startplay',videoType='live')#startDate='2016-05-01',endDate='2017-05-03',,actionType='startplay',screenType='2',ascending=False
	#目前eventType在这个py中只能是play
	obj.play_totalCount(eventType=const.EVENT_PLAY,eventSubType=eventTypeDetail,startDate='2017-06-16',actionType='startplay',screenType='2')


