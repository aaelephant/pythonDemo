#!/usr/local/bin/python

import pandas as pd  
from ggplot import *
 
budget = pd.read_csv("mn-budget-detail-2014.csv")
budget = budget.sort_values('amount',ascending=False)[:10]

p1 = ggplot(budget, aes(x="detail",y="amount"))
p2 = geom_bar(stat="bar", labels=budget["detail"].tolist())
p3 = ggtitle("MN Capital Budget - 2014")
p4 = xlab("Spending Detail")
p5 = ylab("Amount")
p6 = scale_y_continuous(labels='millions')
p7 = theme(axis_text_x=element_text(angle=90))
p = p1 + p2 + p3 + p4 + p5 + p6 + p7
print p

ggsave(p, "mn-budget-capital-ggplot.png")