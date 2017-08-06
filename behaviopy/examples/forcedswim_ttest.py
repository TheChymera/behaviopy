from os import path

from behaviopy.plotting import expandable_ttest

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data/generic")
forced_swim_df_path = path.join(data_dir,"forcedswim_bins.csv")

expandable_ttest(forced_swim_df_path,
	compare="Treatment",
	comparisons={"Interval [minutes]":[]},
	datacolumn_label="Immobility Ratio",
	rename_treatments={"cFluDW":"Fluoxetine","cFluDW_":"Control"},
	save_as="forced_swim_ttest.pdf",
	)

