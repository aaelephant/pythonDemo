#!/usr/bin/python
# -*- coding: UTF-8 -*-

# list = [1,2,3]

# dic = {'a':1, 'b':2}
# for cur in dic:
# 	print dic[cur]

# print 'Prices: '

# while 1:
# 	str = raw_input("请输入：");
# 	print "你输入的内容是: ", str
# 	if (str == "1"):
# 		pass

import os

if os.path.isfile('helo.py'):
	print "this hello.py"
else:
	print 'there is no helo.py'

for letter in 'Python':
   if letter == 'h':
      pass
      print '这是 pass 块'
      print '当前字母 :', letter

print "Good bye!"