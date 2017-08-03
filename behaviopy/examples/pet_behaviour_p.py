from os import path

from behaviopy.regression import correlation_matrix
from behaviopy.abbreviations import *

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data/herde2017")
radioligand_df_path = path.join(data_dir,"SUV_con40-60.csv")
behavior_df_path = path.join(data_dir,"DONOR.csv")

rois = [
	"amygdala",
	"bfs", 
	"brain stem",
	"striatum",
	"cerebellum",
	"central gyrus",
	"inferior colliculus",
	"superior colliculus",
	"cortex", "hippocampus",
	"hypothalamus",
	"midbrain",
	"olfactory",
	"thalamus",
	]
behaviors = [
	"assisted rearing",
	"unassisted rearing",
	"wall walking",
	"center walking",
	"object interaction",
	"body grooming",
	"head grooming",
	"risk assessment",
	"immobility",
	]
animals = [
	"t1",
	"t2",
	"t3",
	"t4",
	"t5",
	]

correlation_matrix(radioligand_df_path,
	df_y_path=behavior_df_path,
	x_cols=rois,
	y_cols=behaviors,
	x_dict=ROI_ABBREV,
	y_dict=BEHAVIOUR_ABBREV,
	entries=animals,
	output="p",
	save_as="pet_behaviour_p.pdf"
	)
