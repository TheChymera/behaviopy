__author__="Horea Christian"
import sys
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from os import path
from sqlalchemy import create_engine, or_, inspection
from sqlalchemy.orm import sessionmaker, aliased, with_polymorphic, joinedload_all

from utils import *

import seaborn as sns
sns.set_style("white", {'legend.frameon': True})

qualitative_colorset = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def sucrose_preference(df, plot_columns=[], legend_loc="best", rename_treatments={}, datacolumn_name="Sucrose Preference Ratio", period_label="Period [days]", save_as=""):

	for key in rename_treatments:
		df.loc[df["treatment"] == key, "treatment"] = rename_treatments[key]

	plt.style.use('ggplot')
	sns.swarmplot(x=period_label,y=datacolumn_name, hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), split=True)
	plt.legend(loc=legend_loc)

	add_significance(df, datacolumn_name, compare="treatment", over=period_label)

	if not save_as:
		plt.show()
