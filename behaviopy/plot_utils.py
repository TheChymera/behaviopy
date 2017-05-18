import collections
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap

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
	label_size = mpl.rcParams['xtick.labelsize']
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

def add_color(cMap, blank_color):
	"""Add a sliver of a given color to a colormap.

	Parameters
	----------

	cMap : array_like
	A matplotlib colormap.

	blank_color : float or string
	Color to add to the colormap (in a matplotlib-comprehensible format).
	"""

	cdict = {
		'red': [],
		'green': [],
		'blue': [],
		'alpha': []
	}

	# regular index to compute the colors
	reg_index = np.linspace(0, 1, 254)

	# shifted index to match the data
	shift_index = np.linspace(0, 1, 256)

	grey_count=0
	grey_shades=2
	for ix, si in enumerate(shift_index):
		grey_count +=1
		if grey_count <= grey_shades:
			cdict['red'].append((si, blank_color, blank_color))
			cdict['green'].append((si, blank_color, blank_color))
			cdict['blue'].append((si, blank_color, blank_color))
			cdict['alpha'].append((si, 1, 1))
		else:
			ri = reg_index[ix-grey_shades]
			r, g, b, a = cMap(ri)
			cdict['red'].append((si, r, r))
			cdict['green'].append((si, g, g))
			cdict['blue'].append((si, b, b))
			cdict['alpha'].append((si, a, a))

	return LinearSegmentedColormap("name", cdict)

def ttp_style(ax, df_,
	padding=0,
	rotate_xticks=True,
	):
	#place and null major ticks (we still need them for the grid)
	ax.xaxis.set_major_locator(ticker.LinearLocator(len(df_.index)+1))
	ax.xaxis.set_major_formatter(ticker.NullFormatter())
	ax.yaxis.set_major_locator(ticker.LinearLocator(len(df_.columns)+1))
	ax.yaxis.set_major_formatter(ticker.NullFormatter())

	#place and format minor ticks (used to substitute for centered major tick labels)
	ax.xaxis.set_minor_locator(ticker.IndexLocator(1,0.5))
	ax.xaxis.set_minor_formatter(ticker.FixedFormatter(df_.index))
	ax.yaxis.set_minor_locator(ticker.IndexLocator(1,0.5))
	ax.yaxis.set_minor_formatter(ticker.FixedFormatter(df_.columns))

	#remove bottom and top small tick lines
	plt.tick_params(axis='x', which='both', bottom='off', top='off', left='off', right='off')
	plt.tick_params(axis='y', which='both', bottom='off', top='off', left='off', right='off')

	#Set only 7th minor tick label to visible
	for label in ax.xaxis.get_minorticklabels():
		label.set_visible(False)
	for label in ax.xaxis.get_minorticklabels()[padding::7]:
		label.set_visible(True)
	for label in ax.yaxis.get_minorticklabels():
		label.set_visible(False)
	for label in ax.yaxis.get_minorticklabels():
		label.set_visible(True)

	#Rotate xticks
	if rotate_xticks:
		plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)

	# create grid
	ax.xaxis.grid(True, which='major', color='1', linestyle='-')
	ax.yaxis.grid(True, which='major', color='1', linestyle='-')

	#delete all spines
	for spine in ["right", "left", "top", "bottom"]:
		ax.spines[spine].set_visible(False)

	return ax
