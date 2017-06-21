#!/usr/local/bin/python

import io
import pandas as pd
import sys

sys.path.append('../../../')

from sql_Module.mysql_const import const
import json
import ijson
import os

class CollectionFile(object):
	"""docstring for CollectionFile"""
	def __init__(self, inputPath):
		super(CollectionFile, self).__init__()
		self.inputPath = inputPath
		
	def getAllDirs(self, folderPath):

		names = [name for name in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, name))]
		return names
	def getAllFiles(self, folderPath):

		names = [name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))]
		return names
	def reWrite(self, filePath, isLast, fo):
		fi = io.open(filePath)
		replaceStr = ''
		if isLast:
			replaceStr = ''
		else:
			replaceStr = ','
		while True:
		    s = fi.read(16*1204)
		    utf8str = s.encode("UTF-8")
		    utf8str = utf8str.replace('[','')
		    utf8str = utf8str.replace(']','')
		    utf8str = utf8str.replace('\n',replaceStr)
		    if not s:
		    	break
		    fo.write(unicode(utf8str,'utf-8'))

		fi.close()
	def collectionFile(self, eventId, dirName):
		# paths = os.path.split(inputPath)
		outFileName = 'log.vr.'+eventId+'.log'
		# print paths
		fo = io.open(os.path.join(self.inputPath,eventId,dirName,outFileName), 'w')
		names = self.getAllFiles(os.path.join(self.inputPath,eventId,dirName))
		for name in names:

			if name == outFileName:
				names.remove(name)
			else:
				
				tests = list(os.path.splitext(name))
				extensionName = tests.pop()
				# print tests
				# print extensionName
				if extensionName != '.log':

					names.remove(name)		
		print names
		lastName = names.pop()
		fo.write(unicode('[',"UTF-8"))
		for name in names:
		    filePath = os.path.join(self.inputPath,eventId,dirName,name)
		    self.reWrite(filePath,False,fo)

		filePath = os.path.join(self.inputPath,eventId,dirName,lastName)

		self.reWrite(filePath,True,fo)
		fo.write(unicode(']',"UTF-8"))
		fo.close()
	def collectionFiles(self, inputPath, eventId):
		dirNames = self.getAllDirs(inputPath)
		for dirName in dirNames:
			self.collectionFile(eventId, dirName)
	def searchDirs(self, inputPath):
		dirNames = self.getAllDirs(inputPath)
		for dirName in dirNames:
			self.collectionFiles(os.path.join(inputPath,dirName), dirName)

	def start(self):
		self.searchDirs(self.inputPath)
if __name__ == '__main__':
	inputPath = '/Users/qbshen/Work/python/Demand/json_logs/output/datas/'
	path = os.path.join(inputPath,'play','20170614/log.vr.play.log')
	collectionFile = CollectionFile(inputPath)
	collectionFile.start()
	# with open(path, 'r') as f:
	#     objects = ijson.items(f, 'item')
	#     columns = list(objects)
	#     jsonStr = json.dumps(columns)
	# df = pd.read_json(path)
	# groupbyuserId = df.groupby([const.COLUMN_VIDEOSID,const.COLUMN_USERID])
	# gr = groupbyuserId.size().to_frame()
	# print gr