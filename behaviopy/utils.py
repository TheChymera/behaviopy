__author__="Horea Christian"
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def add_significance(x1,x2,df, datacolumn, comparison):
	y, h, col = df[datacolumn].max() + 0.1, 0.1, '0.4'
	plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1, c=col)
	compare_values=[]
	for i in comparison:
		compare_values.append(df.loc[(df[list(i)] == pd.Series(i)).all(axis=1)][datacolumn])
	_, p_value = stats.ttest_ind(*compare_values)
	plt.text((x1+x2)*0.5, y+h, "p = {:.2g}".format(p_value), ha='center', va='bottom', color=col)

def rounded_days(datetime_obj):
	days = datetime_obj.days
	# rounding number of days up, as timedelta.days returns the floor only:
	if datetime_obj.seconds / 43199.5 >= 1:
		days += 1
	return days
