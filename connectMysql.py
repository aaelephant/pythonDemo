#!/usr/local/bin/python

import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='312321', db='vr_bi_table_video_play_statistics', cursorclass=MySQLdb.cursors.DictCursor)
cursor = conn.cursor()

cursor.execute('select * from video_play_statistics')
r = cursor.fetchall()
print r