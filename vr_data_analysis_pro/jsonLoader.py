#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import json
import io
from collections import OrderedDict
import os
from pprint import pprint
import pandas as pd
import tarfile
# file = io.open('hello.py', 'r')
# result = file.readall()




# print logStr


class OutLogsData(object):
	"""docstring for OutLogsData"""
	def __init__(self, inputPath, outPath):
		super(OutLogsData, self).__init__()
		self.inputPath = inputPath
		self.outPath = outPath
		
	def readFolder(self, folderPath):
		names = os.listdir(folderPath)

		print names
	def getAllFiles(self, folderPath):

		names = [name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))]
		return names
	def getAllDirs(self, folderPath):

		names = [name for name in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, name))]
		return names
	def readFile(self, filePath):
		with io.open(filePath, 'r') as file:
			result = file.read()
		list = result.split('\n')
		logStr = ''
		for cur in list:
			r = cur.find("\"logs\":")
			if r >= 0:
				logStr = cur
				break
		return logStr
	def parsePlayLogs(self, item):
		itemId = ''
		if item.has_key('itemid'):
			# print 'item'+str(item)
			itemId = item['itemid']
		logInfo = item['logInfo']
		if type(logInfo)!=type({}):
			logInfo = json.loads(logInfo)
		# print logInfo['currentPageId']
		logInfo['itemId'] = itemId
		if logInfo.has_key('currentPageProp'):
			
			eventDic = logInfo['currentPageProp']
			if type(eventDic)!=type({}):
				eventDic = json.loads(eventDic)
			if eventDic.has_key('videoName'):
				logInfo['videoName'] = eventDic['videoName']	
			if eventDic.has_key('videoTags'):
				logInfo['videoTags'] = eventDic['videoName']	
			if eventDic.has_key('curBitType'):
				logInfo['curBitType'] = eventDic['curBitType']	
			if eventDic.has_key('screenType'):
				logInfo['screenType'] = eventDic['screenType']	
			if eventDic.has_key('videoSid'):
				logInfo['videoSid'] = eventDic['videoSid']	
			if eventDic.has_key('videoType'):
				logInfo['videoType'] = eventDic['videoType']	
				
			logInfo.pop('currentPageProp')
		if logInfo.has_key('eventProp'):
			eventProp = logInfo['eventProp']
			if type(eventProp)!=type({}):
				eventProp = json.loads(eventProp)
			if eventProp.has_key('duration'):
				logInfo['duration'] = eventProp['duration']	
			if eventProp.has_key('exitType'):
				logInfo['exitType'] = eventProp['exitType']	
			if eventProp.has_key('playMode'):
				logInfo['playMode'] = eventProp['playMode']	
			if eventProp.has_key('actionType'):
				logInfo['actionType'] = eventProp['actionType']	
			logInfo.pop('eventProp')
		if item.has_key('metadata'):
			metadata = item['metadata']
			if type(metadata)!=type({}):
				metadata = json.loads(metadata)
			if metadata.has_key('sessionId'):
				logInfo['sessionId'] = metadata['sessionId']	
			if metadata.has_key('userId'):
				logInfo['userId'] = metadata['userId']	
				# print 'userId'
			if metadata.has_key('systemName'):
				logInfo['systemName'] = metadata['systemName']	
			if metadata.has_key('apkVersion'):
				logInfo['apkVersion'] = metadata['apkVersion']	
			if metadata.has_key('productModel'):
				logInfo['productModel'] = metadata['productModel']	
			item.pop('metadata')

		return logInfo
	# def parseTopicLogs(self, item):
	# 	itemId = ''
	# 	if item.has_key('itemid'):
	# 		# print 'item'+str(item)
	# 		itemId = item['itemid']
	# 	logInfo = item['logInfo']
	# 	if type(logInfo)!=type({}):
	# 		logInfo = json.loads(logInfo)
	# 	# print logInfo['currentPageId']
	# 	logInfo['itemId'] = itemId
	# 	if logInfo.has_key('currentPageProp'):
			
	# 		eventDic = logInfo['currentPageProp']
	# 		if type(eventDic)!=type({}):
	# 			eventDic = json.loads(eventDic)
	# 		if eventDic.has_key('videoName'):
	# 			logInfo['videoName'] = eventDic['videoName']	
	# 		if eventDic.has_key('videoTags'):
	# 			logInfo['videoTags'] = eventDic['videoName']	
	# 		if eventDic.has_key('curBitType'):
	# 			logInfo['curBitType'] = eventDic['curBitType']	
	# 		if eventDic.has_key('screenType'):
	# 			logInfo['screenType'] = eventDic['screenType']	
	# 		if eventDic.has_key('videoSid'):
	# 			logInfo['videoSid'] = eventDic['videoSid']	
	# 		if eventDic.has_key('videoType'):
	# 			logInfo['videoType'] = eventDic['videoType']	
				
	# 		logInfo.pop('currentPageProp')
	# 	if logInfo.has_key('eventProp'):
	# 		eventProp = logInfo['eventProp']
	# 		if type(eventProp)!=type({}):
	# 			eventProp = json.loads(eventProp)
	# 		if eventProp.has_key('duration'):
	# 			logInfo['duration'] = eventProp['duration']	
	# 		if eventProp.has_key('exitType'):
	# 			logInfo['exitType'] = eventProp['exitType']	
	# 		if eventProp.has_key('playMode'):
	# 			logInfo['playMode'] = eventProp['playMode']	
	# 		if eventProp.has_key('actionType'):
	# 			logInfo['actionType'] = eventProp['actionType']	
	# 		logInfo.pop('eventProp')
	# 	if item.has_key('metadata'):
	# 		metadata = item['metadata']
	# 		if type(metadata)!=type({}):
	# 			metadata = json.loads(metadata)
	# 		if metadata.has_key('sessionId'):
	# 			logInfo['sessionId'] = metadata['sessionId']	
	# 		if metadata.has_key('userId'):
	# 			logInfo['userId'] = metadata['userId']	
	# 			# print 'userId'
	# 		if metadata.has_key('systemName'):
	# 			logInfo['systemName'] = metadata['systemName']	
	# 		if metadata.has_key('apkVersion'):
	# 			logInfo['apkVersion'] = metadata['apkVersion']	
	# 		if metadata.has_key('productModel'):
	# 			logInfo['productModel'] = metadata['productModel']	
	# 		item.pop('metadata')

	# 	return logInfo
	# def parseHomeLogs(self, item):
	# 	# itemId = ''
	# 	# if item.has_key('itemid'):
	# 	# 	# print 'item'+str(item)
	# 	# 	itemId = item['itemid']
	# 	logInfo = item['logInfo']
	# 	if type(logInfo)!=type({}):
	# 		logInfo = json.loads(logInfo)
	# 	# print logInfo['currentPageId']
	# 	# logInfo['itemId'] = itemId
	# 	if logInfo.has_key('currentPageProp'):
			
	# 		eventDic = logInfo['currentPageProp']
	# 		if type(eventDic)!=type({}):
	# 			eventDic = json.loads(eventDic)
	# 		if eventDic.has_key('videoName'):
	# 			logInfo['videoName'] = eventDic['videoName']	
	# 		if eventDic.has_key('videoTags'):
	# 			logInfo['videoTags'] = eventDic['videoName']	
	# 		if eventDic.has_key('curBitType'):
	# 			logInfo['curBitType'] = eventDic['curBitType']	
	# 		if eventDic.has_key('screenType'):
	# 			logInfo['screenType'] = eventDic['screenType']	
	# 		if eventDic.has_key('videoSid'):
	# 			logInfo['videoSid'] = eventDic['videoSid']	
	# 		if eventDic.has_key('videoType'):
	# 			logInfo['videoType'] = eventDic['videoType']	
				
	# 		logInfo.pop('currentPageProp')
	# 	if logInfo.has_key('eventProp'):
	# 		eventProp = logInfo['eventProp']
	# 		if type(eventProp)!=type({}):
	# 			eventProp = json.loads(eventProp)
	# 		if eventProp.has_key('duration'):
	# 			logInfo['duration'] = eventProp['duration']	
	# 		if eventProp.has_key('exitType'):
	# 			logInfo['exitType'] = eventProp['exitType']	
	# 		if eventProp.has_key('playMode'):
	# 			logInfo['playMode'] = eventProp['playMode']	
	# 		if eventProp.has_key('actionType'):
	# 			logInfo['actionType'] = eventProp['actionType']	
	# 		logInfo.pop('eventProp')
	# 	if item.has_key('metadata'):
	# 		metadata = item['metadata']
	# 		if type(metadata)!=type({}):
	# 			metadata = json.loads(metadata)
	# 		if metadata.has_key('sessionId'):
	# 			logInfo['sessionId'] = metadata['sessionId']	
	# 		if metadata.has_key('userId'):
	# 			logInfo['userId'] = metadata['userId']	
	# 			# print 'userId'
	# 		if metadata.has_key('systemName'):
	# 			logInfo['systemName'] = metadata['systemName']	
	# 		if metadata.has_key('apkVersion'):
	# 			logInfo['apkVersion'] = metadata['apkVersion']	
	# 		if metadata.has_key('productModel'):
	# 			logInfo['productModel'] = metadata['productModel']	
	# 		item.pop('metadata')

	# 	return logInfo
	def loadLogsData(self, filePath, pageId):
		with io.open(filePath, 'r') as file:
			result = file.read()
		list = result.split('\n')
		result = []
		for cur in list:
			r = cur.find("\"logs\":")
			if r >= 0:
				# result.append(cur)
				dataDic = json.loads(cur, object_pairs_hook=OrderedDict)

				logs = dataDic['logs']
				
				if type(logs)!=type([]):
					logs = json.loads(logs)
				for item in logs:
					logInfo = ''
					# if pageId == 'play':
					logInfo = self.parsePlayLogs(item)
					# if pageId == 'topic':
						# logInfo = self.parseTopicLogs(item)
					# if pageId == 'home':
						# logInfo = self.parseHomeLogs(item)
					result.append(logInfo)
				
				# logDic = json.loads(logInfo, object_pairs_hook=OrderedDict)
				
				# for logInfo in logs:
					# result.append(logInfo)
		return result
	def findPageID(self, logStr):
		if len(logStr)>0:
	# json_str = json.dumps(logStr)
			dataDic = json.loads(logStr, object_pairs_hook=OrderedDict)
			logs = dataDic['logs']
			logInfo = ''
			if type(logs)==type([]):

				# dataList = json.loads(logs[0])
				logInfo = logs[0]['logInfo']
			else:
				dataList = json.loads(logs)
				logInfo = dataList[0]['logInfo']
			# pprint(logInfo)
			# print type(logInfo)
			currentPageId = ''
			if type(logInfo)==type({}):
				currentPageId = logInfo['currentPageId']	
			else:
				dic = json.loads(logInfo)
				currentPageId = dic['currentPageId']
			return currentPageId
		else:
			print 'no logs'	
			return
	def save(self, dirName, subDirName, fileName, data):
		logs = data
		# fileName = '2017-06-14-08'+'_currentPageId_'+currentPageId+'.log'
		
		# print fileName
		dirPath = self.outPath+dirName
		if os.path.exists(dirPath):
			print dirPath+'is exists'
		else:
			os.mkdir(dirPath)	
		dirPath = os.path.join(dirPath,subDirName)
		if os.path.exists(dirPath):
			print dirPath+'is exists'
		else:
			os.mkdir(dirPath)	
		file = io.open(dirPath+'/'+fileName, 'wb')
		json_str = json.dumps(logs)
		json_str += '\n'
		file.write(json_str)

	def readItemDir(self, dirPath,subDirName):
		fileNames = self.getAllFiles(dirPath)
		for fileName in fileNames:
			filePath = os.path.join(dirPath,fileName)
			
			content = self.readFile(filePath)
			pageId = self.findPageID(content)
			if pageId:
				outFileName = os.path.splitext(fileName)[0]+'_'+pageId+'.log'
				logs = self.loadLogsData(filePath, pageId)
				self.save(pageId,subDirName,outFileName,logs)
	def un_tar(self, file_name, outPutPath):  
		namesSplits = file_name.split('.')
		# dirName = namesSplits[0]
		tar = tarfile.open(file_name)  
		names = tar.getnames()  
		# if os.path.isdir(dirName):  
			# pass  
		# else:  
			# os.mkdir(dirName)  
	#由于解压后是许多文件，预先建立同名文件夹  
		for name in names:  
			tar.extract(name, outPutPath)  
		tar.close() 
	def un_tars(self, inputPath):
		fileNames = self.getAllFiles(inputPath)
		print fileNames
		finalNames = []
		for fileName in fileNames:
			r = fileName.find('.tar.gz')
			print r
			if r>=0:
				finalNames.append(fileName)
		print finalNames
		for finalName in finalNames:
			self.un_tar(os.path.join(inputPath, finalName), inputPath)
	def start(self):
		self.un_tars(self.inputPath)
		dirNames = self.getAllDirs(self.inputPath)
		
		for dirName in dirNames:
			fileDir = os.path.join(self.inputPath,dirName)
			print fileDir
			self.readItemDir(fileDir,dirName)

if __name__ == '__main__':

	outLogsData = OutLogsData('/Users/qbshen/Work/python/Demand/json_logs/input','/Users/qbshen/Work/python/Demand/json_logs/output/datas/')
	outLogsData.start()
# with open(filePath,'r') as f:
# 	data = json.load(f)
# print data
