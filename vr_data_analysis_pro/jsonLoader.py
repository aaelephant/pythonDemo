#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import json
import io
from collections import OrderedDict
import os, shutil, time, datetime
from pprint import pprint
import pandas as pd
import tarfile
from config import config
# file = io.open('hello.py', 'r')
# result = file.readall()




# print logStr


class OutLogsData(object):
	"""docstring for OutLogsData"""
	def __init__(self, inputPath, outputPath):
		super(OutLogsData, self).__init__()
		self.inputPath = inputPath
		self.outputPath = outputPath
		
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
	def parseCurrentPageProp(self, logInfo):
		if logInfo.has_key('currentPageProp'):
			
			eventDic = logInfo['currentPageProp']
			if type(eventDic)!=type({}):
				eventDic = json.loads(eventDic)
			if eventDic.has_key('videoName'):
				logInfo['videoName'] = eventDic['videoName']	
			if eventDic.has_key('videoTags'):
				logInfo['videoTags'] = eventDic['videoTags']	
			if eventDic.has_key('curBitType'):
				logInfo['curBitType'] = eventDic['curBitType']	
			if eventDic.has_key('screenType'):
				logInfo['screenType'] = eventDic['screenType']	
			if eventDic.has_key('videoSid'):
				logInfo['videoSid'] = eventDic['videoSid']	
			if eventDic.has_key('videoType'):
				logInfo['videoType'] = eventDic['videoType']	
				
			logInfo.pop('currentPageProp')
	def parseEventProp(self, logInfo):
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
	def parseMetadata(self, item, logInfo):
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
		if logInfo.has_key('currentPageId') == False:
			logInfo['currentPageId'] = ''
		if logInfo.has_key('happenTime') == False:
			return False
		self.parseCurrentPageProp(logInfo)
		self.parseEventProp(logInfo)
		self.parseMetadata(item, logInfo)
		return logInfo

	def datetime_to_timestamp(self, datetime_obj):
		"""将本地(local) datetime 格式的时间 (含毫秒) 转为毫秒时间戳
	    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
	    :return: 16 位的微秒时间戳  1456402864242
	    """
	    
		local_timestamp = long(time.mktime(datetime_obj.timetuple()) * 1000000.0 + datetime_obj.microsecond)
		return local_timestamp
	def loadLogsData(self, logs, subDirName, fileNamePrefix):
		for item in logs:
			logInfo = ''
			# if pageId == 'play':
			logInfo = self.parsePlayLogs(item)
			# if pageId == 'topic':
				# logInfo = self.parseTopicLogs(item)
			# if pageId == 'home':
				# logInfo = self.parseHomeLogs(item)
			if logInfo == False:
				continue
			itemId = logInfo['itemId']
			pageId = logInfo['currentPageId']
			logDatetime = logInfo['happenTime']
			logtime = time.localtime(float(logDatetime)/1000.0)
			logtimeStr  = time.strftime('%Y%m%d', logtime)
			subDirName = logtimeStr

			local_datetime_now = datetime.datetime.now()
			local_timestamp_now = self.datetime_to_timestamp(local_datetime_now)
			outFileName = fileNamePrefix+'_'+pageId+'_'+str(local_timestamp_now)+'.log'#+str(itemId)+'_'
			logInfos = []
			logInfos.append(logInfo)
			print outFileName
			if pageId:
				self.save(pageId,subDirName,outFileName,logInfos)
	def loadFiles(self, filePath, subDirName):
		with io.open(filePath, 'r') as file:
			result = file.read()
		list = result.split('\n')
		fileName = os.path.basename(filePath)
		prefix = os.path.splitext(fileName)[0]
		# result = []
		for cur in list:
			r = cur.find("\"logs\":")
			if r >= 0:
				# result.append(cur)
				dataDic = json.loads(cur, object_pairs_hook=OrderedDict)

				logs = dataDic['logs']
				
				if type(logs)!=type([]):
					logs = json.loads(logs)
				self.loadLogsData(logs, subDirName, prefix)
					
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
		dirPath = self.outputPath+dirName
		if os.path.exists(dirPath) == False:
			# print ''#dirPath+'is exists'
		# else:
			os.mkdir(dirPath)	
		dirPath = os.path.join(dirPath,subDirName)
		if os.path.exists(dirPath) == False:
			# print ''#dirPath+'is exists'
		# else:
			os.mkdir(dirPath)	
		file = io.open(dirPath+'/'+fileName, 'ab')
		json_str = json.dumps(logs)
		json_str += '\n'
		file.write(json_str)
		file.close()

	def readItemDir(self, dirPath,subDirName):
		fileNames = self.getAllFiles(dirPath)
		for fileName in fileNames:
			filePath = os.path.join(dirPath,fileName)
			self.loadFiles(filePath,subDirName)
			# outFileName = os.path.splitext(fileName)[0]+'_'+pageId++'.log'
			# self.save(pageId,subDirName,outFileName,logs)
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
		if os.path.exists(self.outputPath):
		  	shutil.rmtree(self.outputPath)
			os.mkdir(self.outputPath)
		self.un_tars(self.inputPath)
		dirNames = self.getAllDirs(self.inputPath)
		
		for dirName in dirNames:
			fileDir = os.path.join(self.inputPath,dirName)
			print fileDir
			self.readItemDir(fileDir,dirName)

if __name__ == '__main__':
	json_logs_inputPath = config.configs['inputPath_jsonLoader']
	json_logs_outputPath = config.configs['outputPath_jsonLoader']
	outLogsData = OutLogsData(json_logs_input,json_logs_outputPath)
	outLogsData.start()
# with open(filePath,'r') as f:
# 	data = json.load(f)
# print data
