#!/usr/local/bin/python
#-*- coding:utf8 -*-

import pandas as pd

import sys
sys.path.append('../../')

import sql_Module.connectMysql as conMysql

conms = conMysql.ConnectMysql()
conms.configMdb()

loop = True
chunkSize = 10000000
# chunks = []
chunks = pd.read_sql('select * from video_play_statistics;',\
 con=conms.connector(), chunksize=chunkSize)
# while loop:
#   try:

#     chunks.append(chunk)
#   except StopIteration:
#     loop = False
    # print "Iteration is stopped."
import pdb

# def make_bread():
#     pdb.set_trace()
#     return "I don't have time"

# print(make_bread())
print type(chunks)
# l = list(chunks)
# for df in chunks:
	# df = pd.concat(cur, ignore_index=True)
df = chunks.next()
r=df.groupby(df['videoSid']).size()#count of groupes
# print df

df = chunks.next()
r2=df.groupby(df['videoSid']).size()#count of groupes
# print df
r.append(r2)
print len(r)
df2 = pd.concat(r,chunks.next())
r2=df2.groupby(df2['videoSid']).size()#count of groupes
	break

r.to_excel('out.xlsx', sheet_name='Sheet1',index=True)
for x in xrange(0,9):
	factor = r.iat[x, -1]
factor = r.at['67cdf10792a842b585958a61b3ca0989','id']
factor = list(r.index.values)
factor = list(r.columns.values)
print type(factor)	

print r.loc[factor[0],'videoSid']
by = df[df['videoSid'].isin(factor)]
print by.ix[1:,:1]
budget_plot = r.plot(kind='bar')
fig = budget_plot.get_figure()
fig.savefig("2014-mn-capital-budget.png")

print r
rows = conms.select('select id,date,videoName,userId,videoType,videoSid,actionType,duration  from video_play_statistics limit 0, 10')
mysql_cn= MySQLdb.connect(host='localhost', port=3306,user='myusername', passwd='mypassword', db='mydb')

df = pd.DataFrame( [[ij for ij in i] for i in rows] )

df.rename(columns={0: 'id', 1: 'date', 2: 'videoName', 3: 'userId', 4:'videoType',
	5: 'videoSid', 6:'actionType',
	7: 'duration'}, inplace=True);
df = pd.sort(['duration'], ascending=[1]);

grouped = df.loc[:,df.columns[:6]].groupby(df['videoSid']).describe().reset_index()
r = grouped.size()

grouped.to_excel('out.xlsx', sheet_name='Sheet1',index=True)
grouped = df.groupby(df['videoSid'])
reader = pd.read_csv('data/servicelogs', iterator=True)
try:
    df = reader.get_chunk(100000000)
except StopIteration:
    print "Iteration is stopped."

