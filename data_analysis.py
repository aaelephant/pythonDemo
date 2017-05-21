#!/usr/local/bin/python
#-*- coding:  utf-8 -*-

import sql_Module.connectMysql as conMysql
"""导入sql_Module文件夹下的模块"""


conms = conMysql.ConnectMysql()
conms.main()
# conMysql.()

# import mysql_handle as mysql
"""直接导入同一个目录下的模块"""
# conms = mysql.ConnectMysql()
# conms.main()
