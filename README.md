# BehavioPy

[![Build Status](https://travis-ci.org/TheChymera/behaviopy.svg?branch=master)](https://travis-ci.org/TheChymera/behaviopy)

BehavioPy is a Python toolkit providing evaluation (e.g. event tracking) and plotting functions for behavioural data.
Manual event tracking is done via a simple and configurable PsychoPy-based interface.
Plotting functions are designed to work with preformatted data in CSV format (e.g. as exported by pandas), and use Seaborn and custom BehavioPy styles for maximum beautification.

### Presentations

* [BehavioPy - Python Evaluation, Analysis, and Plotting for Behaviour and Physiology](https://bitbucket.org/TheChymera/behaviopy_repsep/raw/7d626813659efa1345efbf07faafaa9a6bcf3876/poster.pdf), at EuroSciPy 2017 in Erlangen (DE).

## Examples

These are some of the plot types which BehavioPy can generate. 
The following examples can be reproduced (contingent on dependency availability) solely from the [example functions](behaviopy/examples.py) and [data](example_data) distributed in this repository.

### Correlation Matrices

![Correlation Matrix](http://www.chymera.eu/img/examples/behaviopy/corr.png "Correlation Matrix")

![Correlation Matrix Significance](http://www.chymera.eu/img/examples/behaviopy/corr_p.png "")

![Correlation Matrix Significance, Corrected](http://www.chymera.eu/img/examples/behaviopy/corr_pc.png "")

### Pointplot With Significance Levels

![Forced Swim Test Pointplot](http://chymera.eu/img/examples/behaviopy/fst_p.png "")
![Forced Swim Test Pointplot](http://chymera.eu/img/examples/behaviopy/sp_p.png "")

### Timeseries Plots

![Forced Swim Test Timeseries](http://chymera.eu/img/examples/behaviopy/fst_ts.png "")


## Installation

Depending on your preferred package manager you may choose one of the following methods:

#### Portage (e.g. on Gentoo Linux):
SAMRI is available via Portage (the package manager of Gentoo Linux, derivative distributions, and installable on [any other Linux distribution](https://wiki.gentoo.org/wiki/Project:Prefix), or BSD) via the [Science Overlay](https://github.com/getoo/sci).
Upon enabling the overlay, the package can be emerged:

````
emerge behaviopy
````

Alternatively, the live (i.e. latest) version of the package can be installed along with all of its dependencies without the need to enable to overlay:

```
git clone git@github.com:TheChymera/behaviopy.git
cd SAMRI/.gentoo
./install.sh
```

#### Python Package Manager (Users):
Python's `setuptools` allows you to install Python packages independently of your distribution (or operating system, even).
This approach cannot manage any of our numerous non-Python dependencies (by design) and at the moment will not even manage Python dependencies;
as such, given any other alternative, **we do not recommend this approach**:

````
git clone git@github.com:TheChymera/behaviopy.git
cd SAMRI
python setup.py install --user
````

If you are getting a `Permission denied (publickey)` error upon trying to clone, you can either:

* [Add an SSH key](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) to your GitHub account.
* Pull via the HTTPS link `git clone https://github.com/TheChymera/behaviopy.git`.


#### Python Package Manager (Developers):
Python's `setuptools` allows you to install Python packages independently of your distribution (or operating system, even);
it also allows you to install a "live" version of the package - dynamically linking back to the source code.
This permits you to test code (with real module functionality) as you develop it.
This method is sub-par for dependency management (see above notice), but - as a developer - you should be able to manually ensure that your package manager provides the needed packages.

````
git clone git@github.com:TheChymera/behaviopy.git
cd SAMRI
mkdir ~/.python_develop
echo "export PYTHONPATH=\$HOME/.python_develop:\$PYTHONPATH" >> ~/.bashrc
echo "export PATH=\$HOME/.python_develop:\$PATH" >> ~/.bashrc
source ~/.bashrc
python setup.py develop --install-dir ~/.python_develop/
````

If you are getting a `Permission denied (publickey)` error upon trying to clone, you can either:

* [Add an SSH key](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) to your GitHub account.
* Pull via the HTTPS link `git clone https://github.com/TheChymera/behaviopy.git`.


## Dependencies

* [Matplotlib](http://matplotlib.org/)
* [NumPy](http://www.numpy.org/)
* [pandas](http://pandas.pydata.org/)
* [PsychoPy](http://www.psychopy.org/) (optional - only needed for manual event tracking)
* [SciPy](https://www.scipy.org/scipylib/index.html)
* [Seaborn](https://seaborn.pydata.org/)
* [Statsmodels](https://github.com/statsmodels/statsmodels)
