#!/usr/bin/python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
 
budget = pd.read_csv("mn-budget-detail-2014.csv")
budget = budget.sort_values('amount',ascending=False)[:10]
sns.set_style("darkgrid")
bar_plot = sns.barplot(x=budget["detail"],y=budget["amount"],
palette="muted",
x_order=budget["detail"].tolist())
plt.xticks(rotation=90)
plt.show()