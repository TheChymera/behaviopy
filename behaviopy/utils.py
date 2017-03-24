__author__="Horea Christian"
import collections
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from os import path
from scipy import stats

def get_data_dir(subdirectory, data_root_variants):
	"""Get absolute data directory contingent on what variants are available on the system.

	Parameters
	----------

	subdirectory: str
	Which subdirectory (or subsubdirectory, etc.) of the data root is needed

	data_root_variants: list of str
	What data root directories to query (in the given order).
	"""

	my_data_dir = None
	for i in data_root_variants:
		candidate_path = path.abspath(path.expanduser(path.join(i,subdirectory)))
		if path.isdir(candidate_path):
			my_data_dir = candidate_path
			break
	if not my_data_dir:
		raise ValueError("No suitable data directory was found on disk.")

	return my_data_dir

def add_significance(df, datacolumn, compare, over):
	"""Print significance level on 2-item comparison plots (also works with multiple 2-item comparisons)

	Parameters
	----------

	df: pandas_dataframe
		A long-format pandas dataframe containing the data used for the plot.
	datacolumn: string
		The column on which the plotted dimension is located.
	compare: string
		The column over which to perform the t-test comparison (the data frame MUST have two and only two values on this column).
	over: string
		The column over which the plot is repeated. For each value in this column a new t-test is performed. NO correction is performed for multiple comparisons!
	"""


	y, h, col = df[datacolumn].max() + 0.1, 0.1, '0.4'
	comparisons = list(collections.OrderedDict.fromkeys(df[over]))
	compare_categories = list(set(df[compare]))
	line_width = mpl.rcParams['lines.linewidth']
	label_size = mpl.rcParams['axes.labelsize']
	for ix, comparison in enumerate(comparisons):
		compare_vals=[]
		for compare_category in compare_categories:
			compare_category_vals = df.loc[(df[compare] == compare_category) & (df[over] == comparison)][datacolumn]
			compare_vals.append(compare_category_vals)
		compare_vals_lengths = [len(i) for i in compare_vals]
		if 1 in compare_vals_lengths:
			compare_vals = [i for (j,i) in sorted(zip(compare_vals_lengths,compare_vals), reverse=True)]
			_, p_values = stats.ttest_1samp(*compare_vals)
			p_value = p_values[0]
		else:
			_, p_value = stats.ttest_ind(*compare_vals)

		x1 = ix-0.2
		x2 = ix+0.2
		plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=line_width/3, c=col)
		plt.text((x1+x2)*0.5, y+h, "p = {:.2g}".format(p_value), ha='center', va='bottom', color=col, fontsize=label_size)
