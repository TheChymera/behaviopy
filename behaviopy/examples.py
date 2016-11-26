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

if __name__ == '__main__':
	# regression_matrix("~/data/behaviour/DA-PET-Besh/BP.csv", df_y_path="~/data/behaviour/DA-PET-Besh/DONOR.csv", animals=["t1","t2","t3","t4","t5"], output="pearsonr",roi_normalize=False, behav_normalize=False)
	# regression.regression_matrix("~/data/processed/DA-PET-Besh/SUV.csv",
	# 	["cortex", "hippocampus", "striatum", "thalamus", "hypothalamus", "superior colliculus", "inferior colliculus", "midbrain", "brain stem"],
	# 	["assisted rearing", "ambulation", "grooming", "immobility", "object interaction", "unassisted rearing", "risk assessment"],
	# 	df_y_path="~/data/processed/DA-PET-Besh/DONOR.csv",
	# 	animals=["t1","t2","t3","t4","t5"],
	# 	output="pearsonr",
	# 	roi_normalize=False,
	# 	behav_normalize=False,
	# 	save_as="/home/chymera/dvr_r.png",
	# 	)
	regression.regression_matrix("~/data/processed/DA-PET-Besh/SUV_norCb.csv",
		x_dict = roi_dict,
		y_dict = behaviour_dict,
		df_y_path="~/data/processed/DA-PET-Besh/DONOR.csv",
		animals=["t1","t2","t3","t4","t5"],
		output="pearsonr",
		roi_normalize=False,
		behav_normalize=False,
		)
	# regression_matrix("~/data/behaviour/DA-PET-Besh/DVR.csv", df_y_path="~/data/behaviour/DA-PET-Besh/DONOR.csv", animals=["t1","t2","t3","t4","t5"], output="pearsonr",roi_normalize=False, behav_normalize=False,save_as="/home/chymera/dvr_r++.png", xlabel_rotation=45)
	# regression_and_scatter("~/data/behaviour/DA-PET-Besh/DVR.csv", "Objects", ["Thalamus","Striatum","Hippocampus"], animals=["t1","t2","t3","t4","t5"], df_y_path="~/data/behaviour/DA-PET-Besh/DONOR.csv", roi_normalize=False)
	plt.show()
