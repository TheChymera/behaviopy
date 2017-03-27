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
			if isinstance(entry, str):
				notnull_df = df[pd.notnull(df[entry])]
				dates.extend(list(set(notnull_df[entry])))
			if isinstance(entry, dict):
				for key in entry:
					filtered_df = df[df[key] == entry[key][0]]
					for col in entry[key][1:]:
						dates.extend(list(set(filtered_df[col])))
	dates = list(set(dates))
	checked_dates=[]
	for dt in dates:
		try:
			checked_dates.append(dt.date())
		except AttributeError:
			checked_dates.append(dt)
	return checked_dates
