import pandas as pd
from behaviopy import plotting
from os import path

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data/generic")
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

