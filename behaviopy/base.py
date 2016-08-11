import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib import rcParams
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

rcParams.update({'figure.autolayout': True})

behaviour_cols=[u'assisted rearing', u'risk assesment', u'still', u'unassisted rearing', u'Objects', u'Exploration', u'Grooming',u'Exp - no wall', u'Rearing', u'Walking']
pet_cols = [u'Cortex', u'Hippocampus', u'Striatum', u'Thalamus', u'Hypothalamus', u'Superior Colliculus', u'Inferior Colliculus', u'Midbrain', u'Brain Stem']

scatterplot_colors = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

def regression_matrix(df_path, output="pearson", roi_normalize=True, behav_normalize=False):
	df = pd.read_csv(df_path, index_col=0)

	if roi_normalize:
		df[pet_cols] = df[pet_cols].apply(lambda x: (x / x.mean()))
	if behav_normalize:
		df[behaviour_cols] = df[behaviour_cols].apply(lambda x: (x / x.mean()))

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
	ax.tick_params(axis="both",which="both",bottom="off",top="off",length=0)

	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.1)
	cbar = fig.colorbar(im, cax=cax)

def regression_and_scatter(df_path, x_name, y_names, roi_normalize=True, confidence_intervals=False, prediction_intervals=False):
	df = pd.read_csv(df_path, index_col=0)

	if roi_normalize:
		df[pet_cols] = df[pet_cols].apply(lambda x: (x / x.mean()))

	fig, ax = plt.subplots()
	ax.set_xmargin(0.1)
	ax.set_ymargin(0.11)

	for ix, y_name in enumerate(y_names):
		x = df[[x_name]].values
		y = df[[y_name]].values

		x_ = sm.add_constant(x) # constant intercept term
		model = sm.OLS(y, x_)
		fitted = model.fit()
		x_pred = np.linspace(x.min(), x.max(), 50)
		x_pred2 = sm.add_constant(x_pred)
		y_pred = fitted.predict(x_pred2)

		y_hat = fitted.predict(x_)
		y_err = y - y_hat
		mean_x = x.mean()
		n = len(x)
		dof = n - fitted.df_model - 1
		t = stats.t.ppf(0.05, df=dof)
		s_err = np.sum(np.power(y_err, 2))

		if confidence_intervals:
			conf = t * np.sqrt((s_err/(n-2))*(1.0/n + (np.power((x_pred-mean_x),2) / ((np.sum(np.power(x_pred,2))) - n*(np.power(mean_x,2))))))
			upper_conf = y_pred + abs(conf)
			lower_conf = y_pred - abs(conf)
			ax.fill_between(x_pred, lower_conf, upper_conf, color=scatterplot_colors[ix], alpha=0.3)

		if prediction_intervals:
			sdev_pred, lower_pred, upper_pred = wls_prediction_std(fitted, exog=x_pred2, alpha=0.05)
			ax.fill_between(x_pred, lower_pred, upper_pred, color=scatterplot_colors[ix], alpha=0.08)

		data_points = ax.plot(x,y,'o',color=scatterplot_colors[ix],markeredgecolor=scatterplot_colors[ix])
		ax.tick_params(axis="both",which="both",bottom="off",top="off",length=0)
		ax.plot(x_pred, y_pred, '-', color=scatterplot_colors[ix], linewidth=2, label=y_name)
	plt.legend(loc="best")

if __name__ == '__main__':
	plt.style.use('ggplot')
	datafile="~/data/behaviour/besh/Beh vs 18F Dis Ratio.csv"
	# regression_matrix(datafile, output="pearson")
	# regression_matrix(datafile, output="slope")
	regression_and_scatter(datafile, "Objects", ["Thalamus","Striatum","Hippocampus"])
	plt.show()
