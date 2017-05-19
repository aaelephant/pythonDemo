#!/usr/local/bin/python

import pandas as pd
from bokeh.charts import Bar
 
budget = pd.read_csv("mn-budget-detail-2014.csv")
budget = budget.sort_values('amount',ascending=False)[:10]
details = budget["detail"].values.tolist()
amount = list(budget["amount"].astype(float).values)

print 'amount' + str(details)
bar = Bar([1,2,3,4,5], ['dasd','aqeqw','222','eee','rrr','rrrr'], filename="bar.html")
bar.title("MN Capital Budget - 2014").xlabel("Detail").ylabel("Amount")
bar.show()