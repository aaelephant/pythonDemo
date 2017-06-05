#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import pandas as pd

import sys
sys.path.append('../../../')
sys.path.append('../../')

from sql_Module.mysql_const import const
from util import sql_tool
from live_play_entity import LivePlayEntity

from play_statistics_base import PlayStatisticsBase

class DetailPlayStatistics(PlayStatisticsBase):
	"""docstring for DetailPlayStatistics"""
	const.DETAIL_PLAY_COUNT = 'detail_count'
	const.DETAIL_PLAY_USER_COUNT = 'user_count'
	def __init__(self):
		super(DetailPlayStatistics, self).__init__()

	def detail_play_totalCount(self, **kwargs):
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
		self.writetoNewExcle(dataList,'detail_play_statistics')
		return

if __name__ == '__main__':
	obj = DetailPlayStatistics()
	obj.detail_play_totalCount(startDate='2017-05-01',actionType='startplay',screenType='2',ascending=False)	

	