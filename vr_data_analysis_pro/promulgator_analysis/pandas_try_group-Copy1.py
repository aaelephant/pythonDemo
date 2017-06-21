#!/usr/local/bin/python
#-*- coding:utf8 -*-

import pandas as pd

import sys
sys.path.append('../../')

import sql_Module.connectMysql as conMysql

conms = conMysql.ConnectMysql()
conms.configMdb()

loop = True
chunkSize = 10000
# chunks = []
chunks = pd.read_sql('select * from video_play_statistics;', con=conms.connector(), chunksize=chunkSize)
# while loop:
#   try:

#     chunks.append(chunk)
#   except StopIteration:
#     loop = False
    # print "Iteration is stopped."
print type(chunks)
df = pd.concat(chunks[0], ignore_index=True)
r=df.groupby(df['videoSid']).count().ix[:,:]#count of groupes
r.to_excel('out.xlsx', sheet_name='Sheet1',index=True)
# for x in xrange(0,9):
	# factor = r.iat[x, -1]
# factor = r.at['67cdf10792a842b585958a61b3ca0989','id']
# factor = list(r.index.values)
# factor = list(r.columns.values)
# print type(factor)	

# print r.loc[factor[0],'videoSid']
# by = df[df['videoSid'].isin(factor)]
# print by.ix[1:,:1]
# budget_plot = r.plot(kind='bar')
# fig = budget_plot.get_figure()
# fig.savefig("2014-mn-capital-budget.png")

# print r
# rows = conms.select('select id,date,videoName,userId,videoType,videoSid,actionType,duration  from video_play_statistics limit 0, 10')
# mysql_cn= MySQLdb.connect(host='localhost', port=3306,user='myusername', passwd='mypassword', db='mydb')

# df = pd.DataFrame( [[ij for ij in i] for i in rows] )

# df.rename(columns={0: 'id', 1: 'date', 2: 'videoName', 3: 'userId', 4:'videoType',
# 	5: 'videoSid', 6:'actionType',
	# 7: 'duration'}, inplace=True);
# df = pd.sort(['duration'], ascending=[1]);

# grouped = df.loc[:,df.columns[:6]].groupby(df['videoSid']).describe().reset_index()
# r = grouped.size()

# grouped.to_excel('out.xlsx', sheet_name='Sheet1',index=True)
# grouped = df.groupby(df['videoSid'])
# reader = pd.read_csv('data/servicelogs', iterator=True)
# try:
#     df = reader.get_chunk(100000000)
# except StopIteration:
#     print "Iteration is stopped."

