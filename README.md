# BehavioPy

BehavioPy is a python toolkit providing evaluation (e.g. event tracking) and plotting functions for behavioural data.
Manual event tracking is done via a simple and configurable PsychoPy-based interface.
Plotting functions are designed to work with preformatted data in CSV format (e.g. as exported by pandas), and use Seaborn and custom BehavioPy styles for maximum beautification.

# Examples

These are some of the plot types which BehavioPy can generate. 
The following examples can be reproduced (contingent on dependency availability) solely from the [example functions](behaviopy/examples.py) and [data](example_data) distributed in this repository.

## Correlation Matrices

![Correlation Matrix](http://www.chymera.eu/examples/behaviopy/corr.png "Correlation Matrix")
![Correlation Matrix Significance](http://www.chymera.eu/examples/behaviopy/corr_p.png "")
![Correlation Matrix Significance, Corrected](http://www.chymera.eu/examples/behaviopy/corr_pc.png "")

## Pointplot With Significance Levels

![Forced Swim Test Pointplot](http://chymera.eu/examples/behaviopy/fst_p.png "")
![Forced Swim Test Pointplot](http://chymera.eu/examples/behaviopy/sp_p.png "")

## Timeseries Plots

![Forced Swim Test Timeseries](http://chymera.eu/examples/behaviopy/fst_ts.png "")


# Dependencies

* [Matplotlib](http://matplotlib.org/)
* [NumPy](http://www.numpy.org/)
* [pandas](http://pandas.pydata.org/)
* [PsychoPy](http://www.psychopy.org/) (optional - only needed for manual event tracking)
* [SciPy](https://www.scipy.org/scipylib/index.html)
* [Seaborn](https://seaborn.pydata.org/)
* [Statsmodels](https://github.com/statsmodels/statsmodels)
