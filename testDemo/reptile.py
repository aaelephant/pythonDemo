#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Mac OS)'
headers = { 'User-Agent' : user_agent }

try:
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)

	content = response.read().decode('utf-8')
	str1 = '<div class="author clearfix">.*?<a href="/article/(.*?)" target="_blank".*?'#...(.*?)..... item[0]
	str2 = '<a href=".*?<img src="//(.*?)alt=".*?</a>'#...(.*?).... item[1]
	# str3 = '<div.*?class="author.*?src="(.*?)alt'#...(.*?).... item[1]
	pattern = re.compile(str1+str2,re.S)
	items = re.findall(pattern,content)
	print 'items'+str(len(items))
	for item in items:
	# item = items[]
	# print 'item.len:'+str(len(item))+'\n'
	# haveImg = re.search("118996703",item[0])
	# if not haveImg:
		print item[0],item[1]
		

					    
except urllib2.URLError, e:
	if hasattr(e, 'code'):
		print e.code
	if hasattr(e, 'reason'):
		print e.reason