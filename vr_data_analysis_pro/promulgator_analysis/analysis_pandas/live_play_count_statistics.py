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
	def live_play_totalCount(self, **kwargs):
		ascending = True
		if kwargs.has_key('ascending'):
			ascending = kwargs['ascending']
		columns = [const.COLUMN_VIDEOSID,const.COLUMN_USERID]
		chunks = self.installChunks(columns, kwargs)
		df = pd.concat(chunks, ignore_index=False)
		# print type(df)
		groupbyVideoSid = df.groupby(const.COLUMN_VIDEOSID)
		print groupbyVideoSid.size()
		groupbyuserId = df.groupby([const.COLUMN_VIDEOSID,const.COLUMN_USERID])
		gr = groupbyuserId.size().to_frame()
		r = gr.groupby(const.COLUMN_VIDEOSID)
		# print r.size()
		dfVideoSid = groupbyVideoSid.size().sort_values(ascending=False).to_frame()
		dfUserId = r.size().to_frame()
		print dfUserId
		dfUserId.rename(columns={0: 'userCount'}, inplace=True)
		dfMerge = pd.merge(dfVideoSid,dfUserId,left_index=True,right_index=True,how='left')
		print dfMerge
		
		# dfMerge.to_excl("video_play_user.")
		# print len(groupbyVideoSid.size()["62a20fce53c44d6682f959b5df7ae31a"])
# df = df.groupby(by=['column_A'])['column_B'].sum()
# 　　生成的数据类型是Series,如果进一步需要将其转换为dataframe,可以调用Series中的to_frame()方法.
		# groupbyuserId = groupbyVideoSid.apply(const.COLUMN_USERID)
		# print groupbyuserId.size().index
		# groupbyVideoSidMergeUserId = pd.merge(groupbyVideoSid,groupbyuserId, key=const.COLUMN_VIDEOSID)

		# print groupbyVideoSidMergeUserId
		# dfGroupby.rename(columns={0: 'id'}, inplace=True);
		# print dfGroupby.index.values
		columns1 = [const.COLUMN_VIDEOSID,const.COLUMN_VIDEONAME]
		chunksInfo = self.installChunks(columns1,kwargs)
		dfInfo = pd.concat(chunksInfo, ignore_index=False)
		print dfInfo
		dfMergeWithInfo = pd.merge(dfMerge,dfInfo,left_index=True,right_on=const.COLUMN_VIDEOSID,how='left').drop_duplicates()
		dfMergeWithInfo.rename(columns={0: 'playCount'}, inplace=True)
		dfMergeWithInfo = dfMergeWithInfo.reset_index()
		# del dfMergeWithInfo['index']
		print dfMergeWithInfo
		writer = pd.ExcelWriter('output.xlsx')
		dfMergeWithInfo.to_excel(writer,'Sheet1')
		# df2.to_excel(writer,'Sheet2')
		writer.save()
		# for cur in dfMerge:
			# print cur
		return
		
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
	obj.live_play_totalCount(startDate='2016-05-01',videoType='live',actionType='startplay',ascending=False)