#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import data_source as data
import pandas as pd
from sql_Module.mysql_const import const

class CountProgram(object):
	"""docstring for CountProgram"""
	def __init__(self):
		super(CountProgram, self).__init__()

	def initPandas(self):
		df = pd.DataFrame( [[ij for ij in i] for i in rows] )

		df.rename(columns={0: 'id', 1: 'date', 2: 'videoSid'}, inplace=True);
		r=df.groupby(df['videoSid']).count().ix[:,:]#count of groupes

		factor = list(r.columns.values)
		print type(factor)	
	def loadData(self):
		r = data.DataSource()
		def update(r):
			print r
		r.loadData(update, const.COLUMN_ID, const.COLUMN_DATE, const.COLUMN_VIDEOSID, videoSid = 'tvn8opw0c3pq')
	def update(self, data):
		

CountProgram().loadData()
