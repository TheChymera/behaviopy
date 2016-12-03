__author__="Horea Christian"
import sys
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from os import path
from sqlalchemy import create_engine, or_, inspection
from sqlalchemy.orm import sessionmaker, aliased, with_polymorphic, joinedload_all

from .utils import *

import seaborn as sns
sns.set_style("white", {'legend.frameon': True})

qualitative_colorset = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def sucrose_preference(df,
	columns=[],
	legend_loc="best",
	rename_treatments={},
	datacolumn_name="Sucrose Preference Ratio",
	period_label="Period [days]",
	save_as="",
	matplotlibrc=False,
	):

	for key in rename_treatments:
		df.loc[df["treatment"] == key, "treatment"] = rename_treatments[key]

	plt.style.use('ggplot')

	if matplotlibrc:
		matplotlibrc.main()

	sns.swarmplot(x=period_label,y=datacolumn_name, hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), split=True)
	plt.legend(loc=legend_loc)

	add_significance(df, datacolumn_name, compare="treatment", over=period_label)

def forced_swim_ttest(df,
	legend_loc="best",
	rename_treatments={},
	periods={},
	period_label="interval [minutes]",
	plot_behaviour="immobility",
	save_as="",
	matplotlibrc=False,
	):

	for key in rename_treatments:
		df.loc[df["treatment"] == key, "treatment"] = rename_treatments[key]

	plt.style.use('ggplot')

	if matplotlibrc:
		matplotlibrc.main()

	sns.swarmplot(x=period_label, y=plot_behaviour+" ratio", hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), split=True)
	plt.legend(loc=legend_loc)

	add_significance(df, plot_behaviour+" ratio", compare="treatment", over=period_label)

def forced_swim_timecourse(df, is_preformatted=False, legend_loc="best", rename_treatments={}, period_label="interval [1 min]", plotstyle="tsplot", plot_behaviour="immobility", save_as=""):
	for key in rename_treatments:
		df.loc[df["treatment"] == key, "treatment"] = rename_treatments[key]

	plt.style.use('ggplot')
	if plotstyle == "tsplot":
		myplot = sns.tsplot(time=period_label, value=plot_behaviour+" ratio", condition="treatment", unit="identifier", data=df, err_style="unit_traces", color=sns.color_palette(qualitative_colorset))
		myplot.set_xticks(list(set(df[period_label])))
	elif plotstyle == "pointplot":
		sns.pointplot(x=period_label, y=plot_behaviour+" ratio", hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), legend_out=False, dodge=0.1)
	plt.legend(loc=legend_loc)
