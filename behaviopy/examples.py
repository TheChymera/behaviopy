import matplotlib.pyplot as plt

import regression

roi_dict = {
	"amygdala":"Amy",
	"brain stem":"BS",
	"cortex":"Ctx",
	"hippocampus":"HPF",
	"hypothalamus":"HT",
	"inferior colliculus":"IC",
	"midbrain":"MB",
	"striatum":"CPu",
	"superior colliculus":"SC",
	"thalamus":"Tons",
	}

behaviour_dict = {
	"ambulation":"Ambul",
	"assisted rearing":"A. Rear.",
	"body grooming":"Body Grooming",
	"center walking":"Center Walking",
	"exploration":"Exploration",
	"exploration - no wall":"Exp. - no wall",
	"grooming":"Groom.",
	"head grooming":"Head Groom.",
	"immobility":"Immobile",
	"object interaction":"Object",
	"rearing":"Rear.",
	"risk assessment":"Risk",
	"unassisted rearing":"U. Rear.",
	"wall walking":"Wall Walk.",
	}

def arch_besh_da_pet():
	regression.regression_matrix("~/data/processed/DA-PET-Besh/SUV_con40-60.csv",
	x_cols=["amygdala", "bfs", "brain stem", "inferior colliculus", "superior colliculus", "central gyrus", "striatum", "hippocampus", "hypothalamus", "midbrain", "olfactory", "thalamus",],
		y_cols=["assisted rearing", "unassisted rearing", "wall walking", "center walking", "object interaction", "body grooming", "head grooming", "risk assessment", "immobility"],
		x_dict = roi_dict,
		y_dict = behaviour_dict,
		df_y_path="~/data/processed/DA-PET-Besh/DONOR.csv",
		animals=["t1","t2","t3","t4","t5"],
		output="p_corrected",
		roi_normalize=False,
		behav_normalize=False,
		)
	regression.regression_matrix("~/data/processed/DA-PET-Besh/SUV_con40-60.csv",
	x_cols=["amygdala", "bfs", "brain stem", "inferior colliculus", "superior colliculus", "central gyrus", "striatum", "hippocampus", "hypothalamus", "midbrain", "olfactory", "thalamus",],
		y_cols=["assisted rearing", "unassisted rearing", "wall walking", "center walking", "object interaction", "body grooming", "head grooming", "risk assessment", "immobility"],
		x_dict = roi_dict,
		y_dict = behaviour_dict,
		df_y_path="~/data/processed/DA-PET-Besh/DONOR.csv",
		animals=["t1","t2","t3","t4","t5"],
		output="p",
		roi_normalize=False,
		behav_normalize=False,
		)
	regression.regression_matrix("~/data/processed/DA-PET-Besh/SUV_con40-60.csv",
		x_cols=["amygdala", "bfs", "brain stem", "inferior colliculus", "superior colliculus", "central gyrus", "striatum", "hippocampus", "hypothalamus", "midbrain", "olfactory", "thalamus",],
		y_cols=["assisted rearing", "unassisted rearing", "wall walking", "center walking", "object interaction", "body grooming", "head grooming", "risk assessment", "immobility"],
		x_dict = roi_dict,
		y_dict = behaviour_dict,
		df_y_path="~/data/processed/DA-PET-Besh/DONOR.csv",
		animals=["t1","t2","t3","t4","t5"],
		output="pearsonr",
		roi_normalize=False,
		behav_normalize=False,
		)

if __name__ == '__main__':
	arch_besh_da_pet()

	plt.show()
