#!/usr/bin/python

import pandas as pd
 
budget = pd.read_csv("mn-budget-detail-2014.csv")
budget = budget.sort_values('amount',ascending=False)[:10]
pd.options.display.mpl_style = 'default'  
budget_plot = budget.plot(kind="bar",x=budget["detail"],
                          title="MN Capital Budget - 2014",
                          legend=False)
fig = budget_plot.get_figure()
fig.savefig("2014-mn-capital-budget.png")