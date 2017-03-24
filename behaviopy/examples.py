import matplotlib.pyplot as plt
from os import path

import regression
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

if __name__ == '__main__':
	pet_behaviour()

	plt.show()
