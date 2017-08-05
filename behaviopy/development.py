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
