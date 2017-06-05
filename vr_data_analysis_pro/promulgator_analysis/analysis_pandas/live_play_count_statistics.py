#!/usr/local/bin/python
#-*- coding:utf8 -*-

import pandas as pd

import sys
sys.path.append('../../../')
sys.path.append('../../')

from sql_Module.mysql_const import const
from util import sql_tool
from live_play_entity import LivePlayEntity

from play_statistics_base import PlayStatisticsBase

class LivePlayStatistics(PlayStatisticsBase):
	"""docstring for LivePlayStatistics"""
	def __init__(self):
		super(LivePlayStatistics, self).__init__()
		
	def live_play_totalCount(self, **kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		self.whereSql = sql_tool.installFactors(kwargs)
		sql = 'SELECT '\
			  +const.COLUMN_VIDEOSID\
			  +' from '\
			  +const.TABLE_NAME\
			  +self.whereSql
		print sql
		chunks = pd.read_sql(sql,\
	 			 con=self.conms.connector(), chunksize=self.chunkSize)
		df = pd.concat(chunks, ignore_index=False)
		r = df.groupby(const.COLUMN_VIDEOSID).size()
		r = r.sort_values(ascending=ascending)
		dataList = self.installInfo(r)
		self.writetoNewExcle(dataList,'live_play_statistics')
		# for level,subsetDF in r:
		# 	# print level
		# 	r2 = subsetDF.groupby(subsetDF[const.COLUMN_VIDEOSID]).size()
		# 	print r2.iloc[0]

			# break
		# r = r.sort_values(ascending=False)
		# for videoSid in r.index.values:
		
		# print r
		return

if __name__ == '__main__':
	obj = LivePlayStatistics()
	obj.live_play_totalCount(startDate='2017-05-01',videoType='live',actionType='startplay',ascending=False)