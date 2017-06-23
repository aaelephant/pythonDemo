#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import io
import pandas as pd
import sys

sys.path.append('../../')

from sql_Module.mysql_const import const
# file = io.open('hello.py', 'r')
# result = file.readall()

# print result


import json
import ijson
import os

inputPath = '/Users/qbshen/Work/python/Demand/json_logs/output/datas/play/'
path = inputPath + '20170614/log.vr.play.log'
# records = [json.loads(line) for line in open(path)]    
# print records
# import ijson
def getAllDirs(folderPath):

	names = [name for name in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, name))]
	return names
def getAllFiles(folderPath):

	names = [name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))]
	return names
def reWrite(filePath, isLast, fo):
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
	    utf8str = utf8str.replace('n',replaceStr)
	    if not s:
	    	break
	    fo.write(unicode(utf8str,'utf-8'))

	fi.close()
def collectionFile(dirName):
	# paths = os.path.split(inputPath)
	outFileName = 'log.vr.'+'play'+'.log'
	# print paths
	fo = io.open(os.path.join(inputPath,dirName,outFileName), 'w')
	names = getAllFiles(os.path.join(inputPath,dirName))
	for name in names:
		if name == outFileName:
			names.remove(name)
	del names[0]
	lastName = names.pop()
	fo.write(unicode('[',"UTF-8"))
	for name in names:
	    filePath = os.path.join(inputPath,dirName,name)
	    reWrite(filePath,False,fo)

	filePath = os.path.join(inputPath,dirName,lastName)

	reWrite(filePath,True,fo)
	fo.write(unicode(']',"UTF-8"))
	fo.close()
def collectionFiles():
	dirNames = getAllDirs(inputPath)
	for dirName in dirNames:
		collectionFile(dirName)
	
def un_tar(file_name):  
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
		tar.extract(name, '/Users/qbshen/Work/python/Demand/json_logs/')  
	tar.close() 

if __name__ == '__main__':
	import tarfile
	inputPath = '/Users/qbshen/Work/python/Demand/json_logs/'
	fileNames = getAllFiles(inputPath)
	print fileNames
	finalNames = []
	for fileName in fileNames:
		r = fileName.find('.tar.gz')
		print r
		if r>=0:
			finalNames.append(fileName)
	print finalNames
	for finalName in finalNames:
		un_tar(os.path.join(inputPath, finalName))
	# collectionFiles()
	# with open(path, 'r') as f:
	#     objects = ijson.items(f, 'item')
	#     columns = list(objects)
	#     jsonStr = json.dumps(columns)
	# df = pd.read_json(path)
	# groupbyuserId = df.groupby([const.COLUMN_VIDEOSID,const.COLUMN_USERID])
	# gr = groupbyuserId.size().to_frame()
	# print gr
    # objects = ijson.parse(columns[0])
    # objects = ijson.items(columns, 'logs')
    # columns = list(objects)
# print columns[0]

# import json

# json_data = [{'name':'Wang','sal':50000,'job':'VP'},

#  {'name':'Zhang','job':'Manager','report':'VP'},

#  {'name':'Li','sal':5000,'report':[{'a':'va'}]}]

# data_employee = pd.read_json(json.dumps(json_data))

# data_employee_ri = data_employee.reindex(columns=['name','job','sal','report'])

# print data_employee_ri

# with io.open(path, 'r') as file:
	# result = file.read()
# jsonStr = json.loads(result)
# jsonStr = list(jsonStr)
# print jsonStr[0]
# print columns

# groupbyuserId = df.groupby(['log'])
# gr = groupbyuserId.size().to_frame()

# jsonStr = pf['logs'].to_json(orient='index')
# print jsonStr
# print pd.read_json(jsonStr)