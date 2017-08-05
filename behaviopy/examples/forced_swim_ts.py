from os import path

from behaviopy.plotting import forced_swim_timecourse

data_dir = path.join(path.dirname(path.realpath(__file__)),"../../example_data/generic")
forced_swim_df_path = path.join(data_dir,"forcedswim_ts.csv")

forced_swim_timecourse(forced_swim_df_path,
	time_label="Interval [1 min]",
	plotstyle="tsplot",
	datacolumn_label="Immobility Ratio",
	save_as="forced_swim_ts.pdf",
	)

