__author__="Horea Christian"
import pandas as pd
from os import path

def get_data_dir(subdirectory, data_root_variants):
	"""Get absolute data directory contingent on what variants are available on the system.

	Parameters
	----------

	subdirectory: str
		Which subdirectory (or subsubdirectory, etc.) of the data root is needed

	data_root_variants: list of str
		What data root directories to query (in the given order).
	"""

	my_data_dir = None
	for i in data_root_variants:
		candidate_path = path.abspath(path.expanduser(path.join(i,subdirectory)))
		if path.isdir(candidate_path):
			my_data_dir = candidate_path
			break
	if not my_data_dir:
		raise ValueError("No suitable data directory was found on disk.")

	return my_data_dir

def full_subsets(df, minimum_x,
	unit='subject',
	x='Session',
	):
	"""Return a pruned version of the dataframe containing only `unit` slices complete on `x`.

	Parameters
	----------

	df : pandas.DataFrame
		A long-form Pandas Dataframe object which should be pruned.
	minimum_x : str or list
		Either the number of entries on `x` qualifying a unit slice as complete, or a list of values, of which the available values on `x` for each value on `unit` should be a superset, in order for the `unit` slice to qualify as complete.
	unit : str, optional
		Column of `df` along which `df` is to be sliced and tested for completeness.
	x : srt, optional
		Column of `df` on which to check for the presece of sufficient values per `unit` slice.

	Returns
	-------
	df
		A pruned long-form Pandas Dataframe.
	"""
	if minimum_x:
		ids = df[unit].unique()
		for i in ids:
			sliced_df = df[df[unit]==i]
			sessions = sliced_df[x].unique()
			if isinstance(minimum_x, int):
				if len(sessions) < minimum_x:
					df = df[df[unit] != i]
			else:
				if not set(minimum_x).issubset(sessions):
					df = df[df[unit] != i]
	return df

def perdelta(start, end, delta):
	curr = start
	while curr < end:
		yield curr
		curr += delta
	return

def get_dates(df, parameters):
	dates=[]
	for parameter in parameters:
		for entry in parameter:
			if isinstance(entry, dict):
				for key in entry:
					filtered_df = df[df[key] == entry[key][0]]
					for col in entry[key][1:]:
						dates.extend(list(set(filtered_df[col])))
			else:
				notnull_df = df[pd.notnull(df[entry])]
				dates.extend(list(set(notnull_df[entry])))
	dates = list(set(dates))
	checked_dates=[]
	for dt in dates:
		try:
			checked_dates.append(dt.date())
		except AttributeError:
			checked_dates.append(dt)
	return checked_dates
