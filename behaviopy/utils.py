__author__="Horea Christian"
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def add_significance(df, datacolumn, compare, over):
	y, h, col = df[datacolumn].max() + 0.1, 0.1, '0.4'
	comparisons = list(set(df[over]))
	compare_categories = list(set(df[compare]))
	for ix, comparison in enumerate(comparisons):
		compare_vals=[]
		for compare_category in compare_categories:
			compare_category_vals = df.loc[(df[compare] == compare_category) & (df[over] == comparison)][datacolumn]
			compare_vals.append(compare_category_vals)
		_, p_value = stats.ttest_ind(*compare_vals)

		x1 = ix-0.2
		x2 = ix+0.2
		plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1, c=col)
		plt.text((x1+x2)*0.5, y+h, "p = {:.2g}".format(p_value), ha='center', va='bottom', color=col)

def rounded_days(datetime_obj):
	days = datetime_obj.days
	# rounding number of days up, as timedelta.days returns the floor only:
	if datetime_obj.seconds / 43199.5 >= 1:
		days += 1
	return days
