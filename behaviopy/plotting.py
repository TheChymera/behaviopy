__author__="Horea Christian"
import sys
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from os import path
from sqlalchemy import create_engine, or_, inspection
from sqlalchemy.orm import sessionmaker, aliased, with_polymorphic, joinedload_all

try:
	from .utils import *
except ValueError:
	from utils import *

import seaborn as sns
sns.set_style("white", {'legend.frameon': True})

qualitative_colorset = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

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
