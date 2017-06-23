#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import time
import md5
import json

   
timestamp = long(time.time())

url = 'http://showapi-dev.snailvr.com/user/guest_auth?'

payload = {'device_id':'1','model':'1', 'timestamp':str(timestamp)};

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

# a=json.JSONEncoder().encode(payload)
# data=json.dumps(payload)
urlParamsStr = ''
for key in sortKeys:
	urlParamsStr += key+'='+payload[key]+'&'
urlParamsStr = urlParamsStr+'sign'+'='+str(m1.hexdigest())
print 'params:'+urlParamsStr
result = requests.get(url, urlParamsStr);

f = open("cookies.txt", "w") 
f.write(result.cookies['wSvr_2132_userauth']+'')
f.close();
print 'result' + result.text +'\n'+'cookie:'+result.cookies['wSvr_2132_userauth'];