from os import path

from behaviopy.plotting import expandable_ttest

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data/generic")
sucrose_preference_df_path = path.join(data_dir,"sucrosepreference_treatment.csv")

expandable_ttest(sucrose_preference_df_path,
	compare="Sucrose Bottle Position",
	comparisons={"Cage ID":[]},
	datacolumn_label="Sucrose Preference Ratio",
	rename_treatments={"cFluDW":"Fluoxetine","cFluDW_":"Control"},
	save_as="sucrosepreference_side.pdf",
	)

