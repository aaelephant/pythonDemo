#!/usr/local/bin/python

import pandas as pd
from bokeh.charts import Bar , output_file, show
 
budget = pd.read_csv("mn-budget-detail-2014.csv")
budget = budget.sort_values('amount',ascending=False)[:10]
details = budget["detail"].values.tolist()
amount = list(budget["amount"].astype(float).values)

print 'amount' + str(details)
# bar = Bar([1,2,3,4,5], ['dasd','aqeqw','222','eee','rrr','rrrr'])
# bar.title("MN Capital Budget - 2014").xlabel("Detail").ylabel("Amount")
# bar.show()
data = dict(
    python=[2, 3, 7, 5, 26, 221, 44, 233, 254, 265, 266, 267, 120, 111],
    pypy=[12, 33, 47, 15, 126, 121, 144, 233, 254, 225, 226, 267, 110, 130],
    jython=[22, 43, 10, 25, 26, 101, 114, 203, 194, 215, 201, 227, 139, 160],
)
p = Bar(data, label='yr', values='mpg', agg='mean',
       title="Average MPG by YR")

# title("MN Capital Budget - 2014").xlabel("Detail").ylabel("Amount")
output_file("bar.html")

show(p)
# from bokeh.charts import Area, show, output_file

# # create some example data
# data = dict(
#     python=[2, 3, 7, 5, 26, 221, 44, 233, 254, 265, 266, 267, 120, 111],
#     pypy=[12, 33, 47, 15, 126, 121, 144, 233, 254, 225, 226, 267, 110, 130],
#     jython=[22, 43, 10, 25, 26, 101, 114, 203, 194, 215, 201, 227, 139, 160],
# )

# area = Area(data, title="Area Chart", legend="top_left",
#             xlabel='time', ylabel='memory')

# output_file('area.html')
# show(area)