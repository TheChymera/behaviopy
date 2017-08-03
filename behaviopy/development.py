import matplotlib.pyplot as plt
import pandas as pd
from os import path

from abbreviations import *
from utils import get_data_dir

#relative paths
THISSCRIPTSPATH = path.dirname(path.realpath(__file__))
DATA_ROOT_VARIANTS = [
	"~/data/processed/",
	path.join(THISSCRIPTSPATH,"..","example_data"),
	]

def pet_behaviour(
	x_cols=["amygdala", "bfs", "brain stem", "striatum", "cerebellum", "central gyrus", "inferior colliculus", "superior colliculus", "cortex", "hippocampus", "hypothalamus", "midbrain", "olfactory", "thalamus",],
	y_cols=["assisted rearing", "unassisted rearing", "wall walking", "center walking", "object interaction", "body grooming", "head grooming", "risk assessment", "immobility"],
	):

	import regression

	data_dir = get_data_dir("herde2017", DATA_ROOT_VARIANTS)

	regression.regression_matrix(path.join(data_dir,"SUV_con40-60.csv"),
		x_cols=x_cols,
		y_cols=y_cols,
		x_dict = ROI_ABBREV,
		y_dict = BEHAVIOUR_ABBREV,
		df_y_path=path.join(data_dir,"DONOR.csv"),
		animals=["t1","t2","t3","t4","t5"],
		output="p_corrected",
		roi_normalize=False,
		behav_normalize=False,
		)
	regression.regression_matrix(path.join(data_dir,"SUV_con40-60.csv"),
		x_cols=x_cols,
		y_cols=y_cols,
		x_dict = ROI_ABBREV,
		y_dict = BEHAVIOUR_ABBREV,
		df_y_path=path.join(data_dir,"DONOR.csv"),
		animals=["t1","t2","t3","t4","t5"],
		output="p",
		roi_normalize=False,
		behav_normalize=False,
		)
	regression.regression_matrix(path.join(data_dir,"SUV_con40-60.csv"),
		x_cols=x_cols,
		y_cols=y_cols,
		x_dict = ROI_ABBREV,
		y_dict = BEHAVIOUR_ABBREV,
		df_y_path=path.join(data_dir,"DONOR.csv"),
		animals=["t1","t2","t3","t4","t5"],
		output="pearsonr",
		roi_normalize=False,
		behav_normalize=False,
		)

def forced_swim_ttest():
	import plotting

	data_dir = get_data_dir("generic", DATA_ROOT_VARIANTS)
	df_path = path.join(data_dir,"forcedswim_bins.csv")
	df = pd.read_csv(df_path)

	plotting.expandable_ttest(df,
		compare="Treatment",
		comparisons={"Interval [minutes]":[]},
		datacolumn_label="Immobility Ratio",
		rename_treatments={"cFluDW":"Fluoxetine","cFluDW_":"Control"},
		)

def forced_swim_ts(plot_style):
	import plotting

	data_dir = get_data_dir("generic", DATA_ROOT_VARIANTS)
	df_path = path.join(data_dir,"forcedswim_ts.csv")
	df = pd.read_csv(df_path)

	plotting.forced_swim_timecourse(df,
		time_label="Interval [1 min]",
		plotstyle=plot_style,
		datacolumn_label="Immobility Ratio",
		)

def sucrose_preference_treatment():
	import plotting

	data_dir = get_data_dir("generic", DATA_ROOT_VARIANTS)
	df_path = path.join(data_dir,"sucrosepreference_treatment.csv")
	df = pd.read_csv(df_path)

	plotting.expandable_ttest(df,
		compare="Treatment",
		comparisons={"Period [days]":[]},
		datacolumn_label="Sucrose Preference Ratio",
		rename_treatments={"cFluDW":"Fluoxetine","cFluDW_":"Control"},
		)

def sucrose_preference_side():
	import plotting

	data_dir = get_data_dir("generic", DATA_ROOT_VARIANTS)
	df_path = path.join(data_dir,"sucrosepreference_side.csv")
	df = pd.read_csv(df_path)

	plotting.expandable_ttest(df,
		compare="Sucrose Bottle Position",
		comparisons={"Cage ID":[]},
		datacolumn_label="Sucrose Preference Ratio",
		rename_treatments={"cFluDW":"Fluoxetine","cFluDW_":"Control"},
		)

def timetable():
	import plotting

	data_dir = get_data_dir("generic", DATA_ROOT_VARIANTS)
	df_path = path.join(data_dir,"timetable.csv")
	df = pd.read_csv(df_path)

	shade = ["FMRIMeasurement_date"]
	draw = [
		{"TreatmentProtocol_code":["aFluIV","Treatment_start_date"]},
		{"TreatmentProtocol_code":["aFluIV_","Treatment_start_date"]},
		"OpenFieldTestMeasurement_date",
		"ForcedSwimTestMeasurement_date",
		]
	saturate = [
		{"Cage_TreatmentProtocol_code":["cFluDW","Cage_Treatment_start_date","Cage_Treatment_end_date"]},
		{"Cage_TreatmentProtocol_code":["cFluDW_","Cage_Treatment_start_date","Cage_Treatment_end_date"]},
		{"TreatmentProtocol_code":["aFluSC","Treatment_start_date"]},
		]

	plotting.timetable(df, "Animal_id",
		draw=draw,
		saturate=saturate,
		shade=shade,
		window_end="2017,3,21",
		save_plot="timetable.png",
		)

if __name__ == '__main__':
	# timetable()
	#pet_behaviour()
	#forced_swim_ttest()
	#forced_swim_ts("tsplot")
	#forced_swim_ts("pointplot")
	#sucrose_preference_side()
	sucrose_preference_treatment()

	plt.show()
