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
from BaseStatistics import BaseStatistics
from config import config


class PlayStatistics(BaseStatistics):
	"""docstring for PlayStatistics"""
	
	def installColumns(self):
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_USERID]
		return columns

	def videoPlayUserCountDataFrame(self, kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = self.installColumns()
		df = BaseStatistics.installDataFrames(self, columns, kwargs)
		# df = pd.concat(chunks, ignore_index=False)
		groupbyuserId = df.groupby([const.COLUMN_VIDEOSID,const.COLUMN_USERID])
		gr = groupbyuserId.size().to_frame()
		r = gr.groupby(const.COLUMN_VIDEOSID)
		dfUserId = r.size().to_frame()
		dfUserId.rename(columns={0: 'userCount'}, inplace=True)
		# print dfUserId
		return dfUserId

	def mergeVideoPlayCountAndPlayUserCount(self,kwargs):
		df_videoPlayCount = BaseStatistics.videoCountDataFrame(self, kwargs)
		df_videoPlayUserCount = self.videoPlayUserCountDataFrame(kwargs)
		dfMerge = pd.merge(df_videoPlayCount,df_videoPlayUserCount,left_index=True,right_index=True,how='left')
		# print dfMerge
		return dfMerge
			
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
	def paserParams(self,kwargs):
		BaseStatistics.paserParams(self, kwargs)
		if kwargs.has_key(const.COLUMN_SCREENTYPE):

			if kwargs.has_key(const.COLUMN_VIDEOTYPE):
				videoType = kwargs[const.COLUMN_VIDEOTYPE]
				if videoType=='live':
					kwargs[const.COLUMN_SCREENTYPE]='1'
	
	def start(self, **kwargs):
		BaseStatistics.start(self, **kwargs)
		df_merge = self.mergeVideoPlayCountAndPlayUserCount(kwargs)
		# df_videoInfo = self.videoInfoDataFrame(kwargs)
		dfMergeWithInfo = BaseStatistics.installVideoInfo(self, df_merge,kwargs)
		# dfMergeWithInfo = dfMergeWithInfo.set_index(keys=const.COLUMN_VIDEOSID)
		eventSubType = ''
		if kwargs.has_key(const.EVENT_SUB_TYPE):
			eventSubType = kwargs[const.EVENT_SUB_TYPE]
		BaseStatistics.save(self, dfMergeWithInfo, eventSubType)
		# print dfMergeWithInfo
		# fileName = self.to_excel(dfMergeWithInfo)
		# return fileName

if __name__ == '__main__':
	eventTypeDetail = 'detail'
	eventTypeLive = 'live'
	inputPath = config.configs['inputPath']
	obj = PlayStatistics(inputPath)
	# obj.installChunks(videoType='VR',a='a')
	# obj.play_totalCount(eventType=eventTypeLive,startDate='2017-06-16',actionType='startplay',videoType='live')#startDate='2016-05-01',endDate='2017-05-03',,actionType='startplay',screenType='2',ascending=False
	#目前eventType在这个py中只能是play
	obj.start(eventType=const.EVENT_PLAY,eventSubType=eventTypeDetail,startDate='2017-06-01',actionType='startplay',screenType='2')


