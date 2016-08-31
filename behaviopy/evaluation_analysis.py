__author__="Horea Christian"
import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append(os.path.expanduser('~/src/LabbookDB/db/'))
from query import get_df

sns.set_style("darkgrid", {'legend.frameon': True})
qualitative_colorset = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def plot_forced_swim_timecourse(reference_df, is_preformatted=False, plot_columns=[], legend_loc="best", rename_treatments={}, datacolumn_name="Immobility ratio", periodcolumn_name="Period [minute]", periods_label="", plotstyle="tsplot", plot_behaviour="immobility"):
	if not is_preformatted:
		if periods == "minute":
			df = plottable_sums(reference_df, plot_behaviour, identifier_column="Animal_id", periods={0.5:[0,60],1.5:[60,120],2.5:[120,180],3.5:[180,240],4.5:[240,300],5.5:[300,360]})
		elif periods == "2 minutes":
			df = plottable_sums(reference_df, plot_behaviour, identifier_column="Animal_id", periods={1:[0,120],3:[120,240],5:[240,360]})
		else:
			df = plottable_sums(reference_df, plot_behaviour, identifier_column="Animal_id", periods=periods)
	else:
		df = reference_df

	plt.style.use('ggplot')
	# sns.swarmplot(x="period", y="behaviour ratio", hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), split=True)
	if plotstyle == "tsplot":
		sns.tsplot(time="period", value=plot_behaviour+" ratio", condition="treatment", unit="identifier", data=df, err_style="unit_traces", color=sns.color_palette(qualitative_colorset))
		# sns.tsplot(time="period", value=plot_behaviour+" ratio", condition="treatment", unit="identifier", data=df, err_style="unit_traces", color=sns.color_palette(qualitative_colorset), interpolate=False)
	# sns.swarmplot(x="period", y="behaviour ratio", hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset),)
	# sns.pointplot(x="period", y="behaviour ratio", hue="treatment", data=df, palette=sns.color_palette(qualitative_colorset), legend_out=False)
	plt.legend(loc=legend_loc)

def plottable_sums(reference_df, behaviour, identifier_column="Animal_id", periods="", metadata_columns={"TreatmentProtocol_code":"treatment"}):
	identifiers = list(set(reference_df[identifier_column]))
	evaluation_df = pd.DataFrame({})
	for identifier in identifiers:
		identifier_df = reference_df[reference_df[identifier_column]==identifier]
		evaluation_path = identifier_df["Evaluation_path"].values[0]
		identifier_data = {}
		for metadata_column in metadata_columns:
			identifier_data[metadata_columns[metadata_column]] = identifier_df[metadata_column].values[0]
		for period in periods:
			period_start, period_end = periods[period]
			sums = timedelta_sums(evaluation_path, index_name=identifier, period_start=period_start, period_end=period_end)
			#We need to calculate this explicitly since the start/end of th experiment may not align perfecty with the theoretical period
			real_period_duration = sums.sum(axis=1).values[0]
			# if the behaviour key is not found, there was no of that type in the period
			try:
				behaviour_ratio = sums[behaviour].values[0]/real_period_duration
			except KeyError:
				behaviour_ratio = 0
			identifier_data[behaviour+" ratio"] = behaviour_ratio
			identifier_data["period"] = period
			identifier_data["identifier"] = identifier
			period_df_slice = pd.DataFrame(identifier_data, index=[identifier])
			evaluation_df = pd.concat([evaluation_df, period_df_slice])
	return evaluation_df

def timedelta_sums(evaluation_path, index_name="", period_start=False, period_end=False):
	"""Return the per-behaviour sums of timedelta intervals.

	Parameters
	----------

	timedelta_df : pandas_dataframe
		A pandas dataframe containing a "behaviour" and a "timedelta" column
	index_name : string, optional
		The name to add as an index of the retunred series (useful for concatenating multiple outputs)
	period_start : float, optional
		The timepoint
	"""

	timedelta_df = timedeltas(evaluation_path, period_start=period_start, period_end=period_end)
	sums = {}
	for behaviour in list(set(timedelta_df["behaviour"])):
		sums[behaviour] = timedelta_df.loc[timedelta_df["behaviour"] == behaviour, "timedelta"].sum()
	sum_df = pd.DataFrame(sums, index=[index_name])
	return sum_df

def timedeltas(evaluation_path, period_start=False, period_end=False):
	"""Return the per-behaviour sums of timedelta intervals.

	Parameters
	----------

	timedelta_df : pandas_dataframe
		A pandas dataframe containing a "behaviour" and a "timedelta" column
	index_name : string, optional
		The name to add as an index of the retunred series (useful for concatenating multiple outputs)
	period_start : float, optional
		The timepoint
	"""

	df = pd.read_csv(evaluation_path)

	#edit df to fit restricted summary period
	if period_start:
		cropped_df = df[df["start"] > period_start]
		# we perform this check so that the period is not extended beyond the data range
		if not len(cropped_df) == len(df):
			startpoint_behaviour = list(df[df["start"] <= period_start].tail(1)["behaviour"])[0]
			startpoint = pd.DataFrame({"start":period_start,"behaviour":startpoint_behaviour}, index=[""])
			df = pd.concat([startpoint,cropped_df])
	if period_end:
		cropped_df = df[df["start"] < period_end]
		# we perform this check so that the period is not extended beyond the data range
		if not len(cropped_df) == len(df):
			endpoint = pd.DataFrame({"start":period_end,"behaviour":"ANALYSIS_ENDPOINT"}, index=[""])
			df = pd.concat([cropped_df,endpoint])

	# timedelta calculation
	df["timedelta"] = (df["start"].shift(-1)-df["start"]).fillna(0)

	#the last index gives the experiment end time, not meaningful behaviour. We remove that here.
	df = df[:-1]

	return df

if __name__ == '__main__':
	col_entries=[
		("Animal","id"),
		("Cage","id"),
		("Treatment",),
		("TreatmentProtocol","code"),
		("ForcedSwimTestMeasurement",),
		("Evaluation",),
		]
	join_entries=[
		("Animal.cage_stays",),
		("ForcedSwimTestMeasurement",),
		("Evaluation",),
		("CageStay.cage",),
		("Cage.treatments",),
		("Treatment.protocol",),
		]
	# filters = [["Treatment","start_date","2016,4,25,19,30","2016,5,19,23,5"]]
	filters = [["Treatment","start_date","2016,4,25,19,30"]]
	reference_df = get_df("~/syncdata/meta.db",col_entries=col_entries, join_entries=join_entries, filters=filters)
	plot_forced_swim_timecourse(reference_df, legend_loc=4, periods="minute")
	# plot_forced_swim_timecourse(reference_df, legend_loc=4, periods="2 minutes")
	plt.show()
