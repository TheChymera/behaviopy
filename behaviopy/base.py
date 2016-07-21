from string import letters
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
import seaborn as sns
from itertools import product
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

behaviour_cols=[u'assisted rearing', u'risk assesment', u'still', u'unassisted rearing', u'Objects', u'Exploration', u'Grooming',u'Exp - no wall', u'Rearing', u'Walking']
pet_cols = [u'Cortex', u'Hippocampus', u'Striatum', u'Thalamus', u'Hypothalamus', u'Superior Colliculus', u'Inferior Colliculus', u'Midbrain', u'Brain Stem']

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

def regression_matrix(df_path, output="pearson", roi_normalize=True):
	df = pd.read_csv(df_path, index_col=0)

	if roi_normalize:
		df[pet_cols] = df[pet_cols].apply(lambda x: (x / x.mean()))

	if output == "pearson":
		dfc = df.corr()
	if output == "slope":
		dfc = df.corr() * (df.std().values / df.std().values[:, np.newaxis])
	dfc = dfc.loc[behaviour_cols]
	dfc = dfc[pet_cols]

	fig, ax = plt.subplots(figsize=(10, 10))
	im = ax.matshow(dfc, norm=MidpointNormalize(midpoint=0.), cmap=cm.PiYG)
	plt.xticks(range(len(pet_cols)), pet_cols, rotation='vertical')
	plt.yticks(range(len(behaviour_cols)), behaviour_cols)
	ax.grid(False)

	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.1)
	cbar = fig.colorbar(im, cax=cax)

def raw(df_path):
	df = pd.read_csv(df_path, index_col=0)

	x = df[[u'risk assesment']]
	y = df[[u'Inferior Colliculus']]

	y = [2.5,3.8,6.1,7.9,10]
	x = [1,2,3,4,5]

	y = y/np.mean(y)

	print stats.pearsonr(x,y)
	print stats.linregress(x,y)

	fig, ax = plt.subplots()
	ax.plot(x,y,'o')

if __name__ == '__main__':
	# corr_matrix("~/data/behaviour/Beh vs 18F Dis Ratio.csv")
	regression_matrix("~/data/behaviour/Beh vs 18F Dis Ratio.csv")
	# raw("~/data/behaviour/Beh vs 18F Dis Ratio.csv")
	plt.show()
