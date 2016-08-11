import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib import rcParams
import statsmodels.api as sm
from statsmodels.sandbox.stats.multicomp import multipletests
from statsmodels.sandbox.regression.predstd import wls_prediction_std

rcParams.update({
	'figure.autolayout': True,
	'font.family':'sans-serif',
	'font.sans-serif':['Liberation Sans'],
	})
plt.style.use('ggplot')

behaviour_cols=[u'Grooming', u'Objects', u'Assisted Rearing', u'Unassisted Rearing', u'Risk Assesment', u'Still', u'Walking']
pet_cols = [u'Cortex', u'Hippocampus', u'Striatum', u'Thalamus', u'Hypothalamus', u'Superior Colliculus', u'Inferior Colliculus', u'Midbrain', u'Brain Stem']

scatterplot_colors = ["#000000", "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		# Ignoring masked values and all kinds of edge cases...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

def p_from_r(r,n):
	r = max(min(r, 1.0), -1.0)
	df = n-2
	if abs(r) == 1.0:
		prob = 0.0
	else:
		t_squared = r*r * (df / ((1.0 - r) * (1.0 + r)))
		prob = stats.betai(0.5*df, 0.5, df / (df + t_squared))
	return prob

def regression_matrix(df_x_path, df_y_path=None, output="pearson", roi_normalize=True, behav_normalize=False, correction=None, animals=None, save_as=None):

	df = pd.read_csv(df_x_path, index_col=0)

	if df_y_path:
		dfy = pd.read_csv(df_y_path, index_col=0)
		df = pd.concat([df, dfy], axis=1)

	if animals:
		df = df.loc[animals]

	if roi_normalize:
		df[pet_cols] = df[pet_cols].apply(lambda x: (x / x.mean()))
	if behav_normalize:
		df[behaviour_cols] = df[behaviour_cols].apply(lambda x: (x / x.mean()))

	if output == "pearsonr":
		dfc = df.corr()
		cmap = cm.PiYG
	if output == "slope":
		dfc = df.corr() * (df.std().values / df.std().values[:, np.newaxis])
		cmap = cm.PiYG
	if output == "p":
		n = len(df)
		dfc = df.corr()
		dfc = dfc.applymap(lambda x: p_from_r(x,n))
		cmap = cm.BuPu_r

	dfc = dfc.loc[behaviour_cols]
	dfc = dfc[pet_cols]

	if output == "p" and correction:
		dfc_corrected = multipletests(dfc.as_matrix().flatten(), alpha=0.05, method=correction)[1].reshape(np.shape(dfc))
		dfc = pd.DataFrame(dfc_corrected, dfc.index, dfc.columns)

	fig, ax = plt.subplots(figsize=(10, 10))
	if output != "p":
		im = ax.matshow(dfc, norm=MidpointNormalize(midpoint=0.), cmap=cmap)
	else:
		im = ax.matshow(dfc, norm=MidpointNormalize(midpoint=0.05), cmap=cmap)
	plt.xticks(range(len(pet_cols)), pet_cols, rotation='vertical')
	plt.yticks(range(len(behaviour_cols)), behaviour_cols)
	ax.grid(False)
	ax.tick_params(axis="both",which="both",bottom="off",top="off",length=0)

	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = fig.colorbar(im, cax=cax)

	if save_as:
		plt.savefig(save_as,dpi=300)

def regression_and_scatter(df_x_path, x_name, y_names, df_y_path=None, roi_normalize=True, confidence_intervals=False, prediction_intervals=False, animals=None):

	df = pd.read_csv(df_x_path, index_col=0)

	if df_y_path:
		dfy = pd.read_csv(df_y_path, index_col=0)
		df = pd.concat([df, dfy], axis=1)

	if animals:
		df = df.loc[animals]

	if roi_normalize:
		df[pet_cols] = df[pet_cols].apply(lambda x: (x / x.mean()))

	fig, ax = plt.subplots()
	ax.set_xmargin(0.1)
	ax.set_ymargin(0.11)
		df[pet_cols] = df[pet_cols].apply(lambda x: (x / x.mean()))

	fig, ax = plt.subplots()
	ax.set_xmargin(0.1)
	ax.set_ymargin(0.11)

	for ix, y_name in enumerate(y_names):
		x = df[[x_name]].values
		y = df[[y_name]].values

		x_ = sm.add_constant(x) # constant intercept term
		model = sm.OLS(y, x_)

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
	# regression_matrix("~/data/behaviour/besh/BP.csv", df_y_path="~/data/behaviour/besh/DONOR.csv", animals=["t1","t2","t3","t4","t5"], output="pearsonr",roi_normalize=False, behav_normalize=False,save_as="/home/chymera/bp_r.pdf")
	# regression_and_scatter("~/data/behaviour/besh/DVR.csv", "Objects", ["Thalamus","Striatum","Hippocampus"], animals=["t1","t2","t3","t4","t5"], df_y_path="~/data/behaviour/besh/DONOR.csv", roi_normalize=False)
	plt.show()
