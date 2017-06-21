#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../../../')

from sql_Module.mysql_const import const

def installFactors(factors):
			videoSid = ''
			startDate = ''
			endDate = ''
			actionType = ''
			videoType = ''
			screenType = ''
			log_tag = 'has_key:'
			if factors.has_key(const.COLUMN_VIDEOSID):
				print log_tag+const.COLUMN_VIDEOSID
				videoSid = factors[const.COLUMN_VIDEOSID]
			if factors.has_key(const.FACTOR_STARTDATE):
				print log_tag+const.FACTOR_STARTDATE
				startDate = factors[const.FACTOR_STARTDATE]
			if factors.has_key(const.FACTOR_ENDDATE):
				print log_tag+const.FACTOR_ENDDATE
				endDate = factors[const.FACTOR_ENDDATE]
			if factors.has_key(const.COLUMN_ACTIONTYPE):
				print log_tag+const.COLUMN_ACTIONTYPE
				actionType = factors[const.COLUMN_ACTIONTYPE]
			if factors.has_key(const.COLUMN_VIDEOTYPE):
				print log_tag+const.COLUMN_VIDEOTYPE
				videoType = factors[const.COLUMN_VIDEOTYPE]
			if factors.has_key(const.COLUMN_SCREENTYPE):
				print log_tag+const.COLUMN_SCREENTYPE
				screenType = factors[const.COLUMN_SCREENTYPE]
			# tableName = const.TABLE_NAME

			sqls = []
			sql = ''
			
			if len(videoSid)>0:
				factor1 = const.COLUMN_VIDEOSID + const.EQUAL +'\'%s\'' % (videoSid)
				sqls.append(factor1)
			if len(startDate):
				factor2 = const.COLUMN_DATE + const.MORE_EQUAL + '\'%s\'' % (startDate)
				sqls.append(factor2)
			if len(endDate):
				factor3 =  const.COLUMN_DATE + const.LESS_EQUAL + '\'%s\'' % (endDate)
				sqls.append(factor3)
			if len(actionType):
				factor4 = const.COLUMN_ACTIONTYPE+const.EQUAL + '\'%s\'' % (actionType)
				sqls.append(factor4)
			if len(videoType):
				factor5 = const.COLUMN_VIDEOTYPE+const.EQUAL + '\'%s\'' % (videoType)
				sqls.append(factor5)
			if len(screenType):
				factor6 = const.COLUMN_SCREENTYPE+const.EQUAL + '\'%s\'' % (screenType)
				sqls.append(factor6)
			for factor in sqls:
				sql += (factor + const.AND)
			if len(sql):
				sql = ' where ' + sql[0:len(sql)-len(const.AND)]
			return sql