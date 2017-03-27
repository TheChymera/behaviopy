__author__="Horea Christian"
import sys
import time
import datetime as dt
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from os import path
from sqlalchemy import create_engine, or_, inspection
from matplotlib.colors import ListedColormap
from sqlalchemy.orm import sessionmaker, aliased, with_polymorphic, joinedload_all

try:
	from .utils import *
	from .plot_utils import *
except ValueError:
	from utils import *
	from plot_utils import *


import seaborn as sns
sns.set_style("white", {'legend.frameon': True})

qualitative_colorset = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def timetable(reference_df, x_key, shade, saturate,
	colorlist=["0.9","#fff3a3","#a3e0ff","#ffa3ed","#ffa3a3"],
	padding=3,
	real_dates=True,
	window_start="",
	window_end="",
	save_plot=""
	):
	"""Plot a timetable

	Parameters
	----------

	reference_df : Pandas DataFrame
	Dataframe containing the data to plot. It needs to contain columns with datetime values.

	x_key : string
	Column from `reference_df` for the values in which to create rows in the timetable.

	shade: {list of str, list of dict}
	Strings specify the columns for which to shade the datetimes. In dictionaries, the key gives a column to filter by; and if the first item in the value list matches the column value, the datetime in the second item in the value list will specify which datetimes to shade; if the value list contains three items, the datetimes in between that in the second item column and the third item column will be shaded.

	saturate: {list of str, list of dict}
	Strings specify the columns for which to saturate the datetimes. In dictionaries, the key gives a column to filter by; and if the first item in the value list matches the column value, the datetime in the second item in the value list will specify which datetimes to saturate; if the value list contains three items, the datetimes in between that in the second item column and the third item column will be shaded.

	colorlist : list
	A list containing matplotlib-compatible colors to be used for shading.

	padding : int
	Number of days to bad the timetable window with (before and after the first and last scan respectively).

	real_dates : boolean
	Set to False to display dates relative to the first measurement.

	window_start : string
	A datetime-formatted string (e.g. "2016,12,18") to apply as the timetable start date (overrides autodetected start).

	window_end : string
	A datetime-formatted string (e.g. "2016,12,18") to apply as the timetable end date (overrides autodetected end).
	"""

	#truncate dates
	for col in reference_df.columns:
		if "date" in col:
			#the following catches None entries:
			try:
				reference_df[col] = reference_df[col].apply(lambda x: x.date())
			except AttributeError:
				pass

	#GET FIRST AND LAST DATE
	dates = get_dates(reference_df, [shade, saturate])
	if not window_start:
		window_start = min(dates) - dt.timedelta(days=padding)
	else:
		window_start = dt.strptime(window_start, "%Y,%m,%d").date()
	if not window_end:
		window_end = max(dates) + dt.timedelta(days=padding)
	else:
		window_end = dt.strptime(window_end, "%Y,%m,%d").date()

	#create generic plotting dataframe
	x_vals = list(set(reference_df[x_key]))
	datetime_index = [i for i in perdelta(window_start,window_end,dt.timedelta(days=1))]

	df = pd.DataFrame(index=datetime_index, columns=x_vals)
	df = df.fillna(0)

	#set plotting params
	cMap = add_color(cm.viridis, 0.9)
	fig_shape = (df.shape[0],df.shape[1]/1.5) #1.5 seems like a good scaling value to make cells not-too-tall and not-too-short
	fig, ax = plt.subplots(figsize=fig_shape , facecolor='#eeeeee', tight_layout=True)

	#populate frames
	df_ = df.copy(deep=True)
	for c_step, entry in enumerate(shade):
		c_step += 1
		for x_val in x_vals:
			if isinstance(entry, dict):
				for key in entry:
					start=False #unless the code below is succesful, no attempt is made to add an entry for the x_val
					filtered_df = reference_df[(reference_df[key] == entry[key][0])&(reference_df[x_key] == x_val)]
					try:
						start = list(set(filtered_df[entry[key][1]]))[0]
					except IndexError:
						pass
					if len(entry[key]) == 3:
						end = list(set(filtered_df[entry[key][2]]))[0]
						active_dates = [i for i in perdelta(start,end+dt.timedelta(days=1),dt.timedelta(days=1))]
						for active_date in active_dates:
							df_.set_value(active_date, x_val, df_.get_value(active_date, x_val)+c_step)
					elif start:
						df_.set_value(start, x_val, df_.get_value(start, x_val)+c_step)
			elif isinstance(entry, str):
				filtered_df = reference_df[reference_df[x_key] == x_val]
				active_dates = list(set(filtered_df[entry]))
				for active_date in active_dates:
					#escaping dates which are outside the date range (e.g. when specifying tighter window_end and window_start contraints)
					try:
						df_.set_value(active_date, x_val, df_.get_value(active_date, x_val)+c_step)
					except KeyError:
						pass
	if not real_dates:
		df_ = df_.set_index(np.arange(len(df_))-padding)
	im = ax.pcolorfast(df_.T, cmap=add_color(cm.gray_r, 0.8), alpha=.5)
	plt.hold(True)

	#populate frames
	df_ = df.copy(deep=True)
	for c_step, entry in enumerate(saturate):
		c_step += 1
		for x_val in x_vals:
			if isinstance(entry, dict):
				for key in entry:
					filtered_df = reference_df[(reference_df[key] == entry[key][0])&(reference_df[x_key] == x_val)]
					try:
						start = list(set(filtered_df[entry[key][1]]))[0]
						try:
							start = start.date()
						except AttributeError:
							pass
					except IndexError:
						pass
					if len(entry[key]) == 3:
						try:
							end = list(set(filtered_df[entry[key][2]]))[0]
							active_dates = [i for i in perdelta(start,end+dt.timedelta(days=1),dt.timedelta(days=1))]
							for active_date in active_dates:
								df_.set_value(active_date, x_val, df_.get_value(active_date, x_val)+c_step)
						except IndexError:
							pass
					elif start:
						df_.set_value(start, x_val, df_.get_value(start, x_val)+c_step)
					# we need this to make sure start does not remain set for the next iteration:
					start=False
			elif isinstance(entry, str):
				filtered_df = reference_df[reference_df[x_key] == x_val]
				active_dates = list(set(filtered_df[entry]))
				df_.set_value(active_dates, x_val, 1)
	if not real_dates:
		df_ = df_.set_index(np.arange(len(df_))-padding)
	im = ax.pcolorfast(df_.T, cmap=ListedColormap(colorlist), vmin=0, vmax=len(colorlist)-1, alpha=.5)
	plt.hold(True)

	if real_dates:
		ax = ttp_style(ax, df_)
	else:
		ax = ttp_style(ax, df_, padding)
		plt.xlabel("Days")
	plt.ylabel(" ".join(x_key.split("_")).replace("id","ID"))

	if save_plot:
		plt.savefig(path.abspath(path.expanduser(save_plot)), bbox_inches='tight')

def control_first_reordering(df, hue_column):
	"""Reorder the dataframe so that rows with control data show up first (this makes Seaborn assign them the first colors in the colorset).

	Parameters
	----------

	df : pandas DataFrame
	Dataframe to reorder

	hue_column : string
	The name of the column based on which the hue will be applied. This is the column which must indicate which rows correspond to controls
	"""

	hue_ordering = []
	noncontrols = []
	for hue in list(set(df[hue_column])):
		if "Control" in hue or "control" in hue:
			hue_ordering.append(hue)
		else:
			noncontrols.append(hue)
	hue_ordering.extend(noncontrols)
	df[hue_column] = pd.Categorical(df[hue_column], hue_ordering)
	df.sort(hue_column)

	return df

def expandable_ttest(df,
	compare="Treatment",
	comparisons={"Period [days]":[]},
	datacolumn_label="Sucrose Preference Ratio",
	legend_loc="best",
	rename_treatments={},
	):
	"""High-level interface for plotting of one or multiple related t-tests.

	Parameters
	----------

	df : Pandas Dataframe
	Pandas Dataframe containing the experimental data.

	compare : string, optional
	Which parameter to categorize the comparison by. Must be a column name from df.

	comparisons : dict, optional
	A dictionary, the key of which indicates which df column to generate comparison insances from. If only a subset of the available rows are to be included in the comparison, the dictionary needs to specify a value, consisting of a list of acceptable values on the column given by the key.

	datacolumn_label : string, optional
	A column name from df, the values in which column give the data to plot.

	legend_loc : string, optional
	Where to place the legend on the figure.

	rename_treatments : dict, optional
	Dictionary with strings as keys and values used to map treatment names onto new stings.
	"""

	comparison_instances_label = list(comparisons.keys())[0]
	comparison_instances = list(comparisons.values())[0]
	if comparison_instances:
		df[df[comparison_instances_label].isin([comparison_instances])]

	if rename_treatments:
		for key in rename_treatments:
			df.loc[df["Treatment"] == key, "Treatment"] = rename_treatments[key]
		df = control_first_reordering(df, "Treatment")

	plt.style.use('ggplot')
	sns.swarmplot(x=comparison_instances_label,y=datacolumn_label, hue=compare, data=df, palette=sns.color_palette(qualitative_colorset), split=True)
	plt.legend(loc=legend_loc)

	add_significance(df, datacolumn_label, compare=compare, over=comparison_instances_label)

def forced_swim_timecourse(df,
	datacolumn_label="Immobility Ratio",
	legend_loc="best",
	plotstyle="tsplot",
	rename_treatments={},
	time_label="interval [1 min]",
	):
	"""Plot timecourse of forced swim measurements.

	Parameters
	----------

	df : Pandas Dataframe
	Pandas Dataframe containing the experimental data.

	datacolumn_label : string, optional
	A column name from df, the values in which column give the data to plot.

	legend_loc : string, optional
	Where to place the legend on the figure.

	plotstyle : {"pointplot", "tsplot"}
	Dictionary with strings as keys and values used to map treatment names onto new stings.

	rename_treatments : dict, optional
	Dictionary with strings as keys and values used to map treatment names onto new stings.

	time_label : dict, optional
	A column name from df, the values in which column give the time pointd of the data.
	"""

	for key in rename_treatments:
		df.loc[df["Treatment"] == key, "Treatment"] = rename_treatments[key]
	df = control_first_reordering(df, "Treatment")

	plt.style.use('ggplot')
	if plotstyle == "tsplot":
		myplot = sns.tsplot(time=time_label, value=datacolumn_label, condition="Treatment", unit="Identifier", data=df, err_style="unit_traces", color=sns.color_palette(qualitative_colorset))
		myplot.set_xticks(list(set(df[time_label])))
	elif plotstyle == "pointplot":
		sns.pointplot(x=time_label, y=datacolumn_label, hue="Treatment", data=df, palette=sns.color_palette(qualitative_colorset), legend_out=False, dodge=0.1)
	plt.legend(loc=legend_loc)
