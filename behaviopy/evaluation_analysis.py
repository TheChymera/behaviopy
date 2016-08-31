import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.expanduser('~/src/LabbookDB/db/'))
from query import get_df

def sums_plot(evaluation_path):
	timedelta_df = timedeltas(evaluation_path)
	sum_df = timedelta_sums(timedelta_df, index="nd750_a0037_0-24")


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
		startpoint_behaviour = list(df[df["start"] <= period_start].tail(1)["behaviour"])[0]
		startpoint = pd.DataFrame({"start":period_start,"behaviour":startpoint_behaviour}, index=[""])
		# it is important that the df slice is done with > and not >=
		# otherwise in select cases the above startpoint definition becomes redundant and confusing
		df = df[df["start"] > period_start]
		df = pd.concat([startpoint,df])
	if period_end:
		df = df[df["start"] < period_end]
		endpoint = pd.DataFrame({"start":period_end,"behaviour":"ANALYSIS_ENDPOINT"}, index=[""])
		df = pd.concat([df,endpoint])

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

	# timedelta_sums("~/data/behaviour/forced_swim_test/nd750_a0037_0-24_chr.csv", period_start=300, period_end=320)
