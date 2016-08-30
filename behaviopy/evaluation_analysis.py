import pandas as pd
import numpy as np

def timedelta_sums(evaluation_path, index_name=""):
	df = timedeltas(evaluation_path)
	print df
	sums = {}
	for behaviour in list(set(df["behaviour"])):
		print behaviour
		sums[behaviour] = df.loc[df["behaviour"] == behaviour, 'timedelta'].sum()
	sum_df = pd.DataFrame(sums, index=[index_name])
	print sum_df

def timedeltas(evaluation_path):
	df = pd.read_csv(evaluation_path)
	df['timedelta'] = (df['start'].shift(-1)-df['start']).fillna(0)
	df = df[:-1] #the last index gives the experiment end time, not meaningful behaviour
	return df


if __name__ == '__main__':
	timedelta_sums("~/data/behaviour/forced_swim_test/nd750_a0037_0-24_chr.csv")
