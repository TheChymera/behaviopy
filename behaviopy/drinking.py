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

sys.path.append('/home/chymera/src/LabbookDB/db/')
from common_classes import *
from query import loadSession, allowed_classes, get_df

import seaborn as sns
sns.set_style("white", {'legend.frameon': True})

qualitative_colorset = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def plottable_sucrosepreference_df(reference_df):
	cage_ids = list(set(reference_df["Cage_id"]))
	preferences_df = pd.DataFrame({})
	for cage_id in cage_ids:
		cage_id_df = reference_df[reference_df["Cage_id"]==cage_id]
		reference_dates = list(set(cage_id_df["SucrosePreferenceMeasurement_reference_date"]))
		reference_dates.sort()
		measurement_dates = list(set(cage_id_df["SucrosePreferenceMeasurement_date"]))
		measurement_dates.sort()
		first_date = reference_dates[0]
		preferences={}
		for measurement_date in measurement_dates:
			cage_id_measurement_df = cage_id_df[cage_id_df["SucrosePreferenceMeasurement_date"] == measurement_date]
			start_date = cage_id_measurement_df["SucrosePreferenceMeasurement_reference_date"].tolist()[0]
			relative_start_day = start_date-first_date
			rounded_relative_start_day = rounded_days(relative_start_day)
			relative_end_day = measurement_date-first_date
			rounded_relative_end_day = rounded_days(relative_end_day)
			key = "{} to {}".format(rounded_relative_start_day, rounded_relative_end_day)
			water_start = cage_id_measurement_df["SucrosePreferenceMeasurement_water_start_amount"].tolist()[0]
			water_end = cage_id_measurement_df["SucrosePreferenceMeasurement_water_end_amount"].tolist()[0]
			sucrose_start = cage_id_measurement_df["SucrosePreferenceMeasurement_sucrose_start_amount"].tolist()[0]
			sucrose_end = cage_id_measurement_df["SucrosePreferenceMeasurement_sucrose_end_amount"].tolist()[0]
			water_consumption = water_end - water_start
			sucrose_consumption = sucrose_end - sucrose_start
			sucrose_prefernce = sucrose_consumption/(water_consumption + sucrose_consumption)
			preferences["Period [days]"] = key
			preferences["Sucrose Preference Ratio"] = sucrose_prefernce
			preferences["treatment"] = cage_id_measurement_df["TreatmentProtocol_code"].tolist()[0]
			preferences["cage id"] = cage_id # this may not actually be needed, as the same info is contained in the index
			preferences_df_slice = pd.DataFrame(preferences, index=[cage_id])
			preferences_df = pd.concat([preferences_df, preferences_df_slice])

	return preferences_df

def sucrosepreference_plot(reference_df, is_preformatted=False, plot_columns=[], legend_loc="best", rename_treatments={}, datacolumn_name="Sucrose Preference Ratio", period_label="Period [days]"):

	if not is_preformatted:
		df = plottable_sucrosepreference_df(reference_df)
	else:
		df = reference_df

	for key in rename_treatments:
		df.loc[df["treatment"] == key, "treatment"] = rename_treatments[key]

	plt.style.use('ggplot')
	sns.swarmplot(x=period_label,y=datacolumn_name, hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), split=True)
	plt.legend(loc=legend_loc)

	add_significance(-0.2,0.2,df,datacolumn_name,[{period_label:"0 to 2","treatment":"Control"},{period_label:"0 to 2","treatment":"Fluoxetine"}])
	add_significance(0.8,1.2,df,datacolumn_name,[{period_label:"2 to 5","treatment":"Control"},{period_label:"2 to 5","treatment":"Fluoxetine"}])

if __name__ == '__main__':
	col_entries=[
		("Cage","id"),
		("Treatment",),
		("SucrosePreferenceMeasurement",),
		("TreatmentProtocol","code"),
		]
	join_entries=[
		("Cage.treatments",),
		("SucrosePreferenceMeasurement",),
		("Treatment.protocol",),
		]
	filters = [["Treatment","start_date","2016,4,25,19,30","2016,5,19,23,5"]]
	reference_df = get_df("~/syncdata/meta.db",col_entries=col_entries, join_entries=join_entries, filters=filters)

	sucrosepreference_plot(reference_df, plot_columns=["0 to 2", "2 to 5"],legend_loc=4, rename_treatments={"cFluDW":"Fluoxetine","cFluDW_":"Control"})
	plt.show()
