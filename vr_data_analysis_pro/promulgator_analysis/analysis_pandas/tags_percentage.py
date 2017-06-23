#!/usr/local/bin/python
#-*- coding:utf-8 -*-

#oneStep:
#	计算所选时间内，所有标签出现的总数
#twoStep:
# 	计算每一个标签出现的总数
#threeStep:
#	计算每一个标签对于所有标签的占比数

import sys, math
import pandas as pd
sys.path.append('../../../')
# import MySQLdb

sys.path.append('../../')

from config import config
from sql_Module.mysql_const import const
from BaseStatistics import BaseStatistics

COLUMN_COUNT = 'count'
COLUMN_NAME = 'name'

class TagsPercentage(BaseStatistics):
	"""docstring for TagsPercentage"""
	# def __init__(self, inputPath):
	# 	super(TagsPercentage, self).__init__(inputPath)
	# 	self.inputPath = inputPath
	
	def countTags(self, tagDics):
		df = pd.DataFrame(tagDics)
		df = df.groupby(df[COLUMN_NAME])
		tagsSum = df.sum()
		# print tagsSum.pct_change()
		tagsSumDF = tagsSum.sort_values(by=COLUMN_COUNT, ascending=False)
		tagsSumDF = tagsSumDF.reset_index()
		
		tagsSumSeries = tagsSumDF[COLUMN_COUNT] / tagsSumDF[COLUMN_COUNT].sum()

		pctDF = tagsSumSeries.to_frame()
		resultDF = pd.merge(tagsSumDF,pctDF,left_index=True,right_index=True,how='left').drop_duplicates()
		return resultDF
	def loadTagItem(self, tagItem, playCount):
		tagDics = []

		if tagItem == tagItem:
			if tagItem == '':
				return tagDics
			tagItems = tagItem.split('-')
			for tag in tagItems:
				itemDic = {}
				itemDic[COLUMN_NAME] = tag
				itemDic[COLUMN_COUNT] = playCount	
				tagDics.append(itemDic)
		return tagDics

	def loadTags(self, df):
		tagDics = []
		for index in df.index.values:
			# print index
			
			tagItem = df.at[index, const.COLUMN_VIDEOTAGS]
			playCount = df.loc[index, 'playCount']
			curTagDics = self.loadTagItem(tagItem, playCount)
			tagDics = tagDics+curTagDics
		resultDF = self.countTags(tagDics)
		return resultDF

	def start(self, **kwargs):
		BaseStatistics.start(self,**kwargs)
		df = super(TagsPercentage, self).videoCountDataFrame(kwargs)
		df = BaseStatistics.installVideoInfo(self, df, kwargs)
		resultDF = self.loadTags(df)
		BaseStatistics.save(self, resultDF, 'tags')
	

if __name__ == '__main__':
	inputPath = config.configs['inputPath']
	tagsP = TagsPercentage(inputPath)
	tagsP.start(eventType=const.EVENT_PLAY, startDate='2017-06-22')



