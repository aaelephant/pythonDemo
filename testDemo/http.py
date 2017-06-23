#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time
import md5
import json
import random
import string




class DanmuSender:

   def __init__(self):
   		# print 'create'
   		return
   def printme(self, msg ):
   
 
		timestamp = long(time.time())

		f = open("cookies.txt", "r") 
		text = f.read()
		f.close();

		cookies = dict(wSvr_2132_userauth=text)
		payload = {'roomid':'11','message':msg, 'timestamp':str(timestamp)};

		originStr = ''
		allkeys = payload.keys()



		sortKeys = sorted(allkeys)

		for i in xrange(0,len(sortKeys)):
			print 'key' + sortKeys[i];

		for key in sortKeys:
			originStr += key+'='+payload[key]+'&'
		originStr = originStr[0:len(originStr)-1]+'SHOW_SNAILVR_AUTHENTICATION'

		originStr = originStr.decode("UTF-8" )
		print 'str:'+originStr

		m1 = md5.new()   
		m1.update(originStr)   

		print m1.hexdigest()   

		payload['sign']= str(m1.hexdigest())

		data = json.dumps(payload)

		result = requests.post("http://showapi-dev.snailvr.com///room/danmaku", data, cookies=cookies)

		print "result" + result.text


sender = DanmuSender()
while 1:

	time.sleep(0.01)
	
	random_str = ''.join([random.choice(string.ascii_letters) for i in range(16)])

	sender.printme(random_str)	