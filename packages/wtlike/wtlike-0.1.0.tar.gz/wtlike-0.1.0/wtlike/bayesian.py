# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/14_bayesian.ipynb (unless otherwise specified).

__all__ = ['CountFitness', 'LikelihoodFitness', 'doc_countfitness', 'get_bb_partition', 'bb_overplot', 'WtLike', 'BBA']

# Cell
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.stats.bayesian_blocks import FitnessFunc

from .config import *
from .lightcurve import * #get_lightcurve, fit_cells, flux_plot
from .cell_data import * #get_cells, partition_cells
from .loglike import *

plt.rc('font', size=18)

# Cell
class CountFitness(FitnessFunc):
    """
    Adapted version of a astropy.stats.bayesian_blocks.FitnessFunc
    Considerably modified to give the `fitness function` access to the cell data.

    Implements the Event model using exposure instead of time.

    """

    def __init__(self, lc, p0=0.05,):
        """
        - lc  -- a LightCurve data table, with  exposure (e) and counts (n),
            as well as a representation of the likelihood for each cell
        - p0 --
        """
        self.p0=p0
        self.df= df= lc
        N = self.N = len(df)
        # Invoke empirical function from Scargle 2012
        self.ncp_prior = self.p0_prior(N)

        #actual times for bin edges
        t = df.t.values
        dt = df.tw.values/2
        self.mjd = np.concatenate([t-dt, [t[-1]+dt[-1]] ] ) # put one at the end
        self.name = self.__class__.__name__
        self.setup()

    def setup(self):
        df = self.df

        # counts per cell
        self.nn = df.n.values
        assert min(self.nn)>0, 'Attempt to Include a cell with no contents'

        # edges and block_length use exposure as "time"
        e = df.e.values
        self.edges = np.concatenate([[0], np.cumsum(e)])
        self.block_length = self.edges[-1] - self.edges

    def __str__(self):

        return f'{self.name}: {self.N} cells, spanning {self.block_length[0]:.1f} days, prior={self.ncp_prior:.1f}'

    def __call__(self, R):
        """ The fitness function needed for BB algorithm
        For cells 0..R return array of length R+1 of the maximum log likelihoods for combined cells
        0..R, 1..R, ... R
        """
        # exposures and corresponding counts
        w_k = self.block_length[:R + 1] - self.block_length[R + 1]
        N_k = np.cumsum(self.nn[:R + 1][::-1])[::-1]

        # Solving eq. 26 from Scargle 2012 for maximum $\lambda$ gives
        return N_k * (np.log(N_k) - np.log(w_k))

    def fit(self):
        """Fit the Bayesian Blocks model given the specified fitness function.
        Refactored version using code from bayesian_blocks.FitnesFunc.fit
        Returns
        -------
        edges : ndarray
            array containing the (M+1) edges, in MJD units, defining the M optimal bins
        """
        # This is the basic Scargle algoritm, copied almost verbatum
        # ---------------------------------------------------------------

        # arrays to store the best configuration
        N = self.N
        best = np.zeros(N, dtype=float)
        last = np.zeros(N, dtype=int)

        # ----------------------------------------------------------------
        # Start with first data cell; add one cell at each iteration
        # ----------------------------------------------------------------
        for R in range(N):

            # evaluate fitness function
            fit_vec = self(R)

            A_R = fit_vec - self.ncp_prior
            A_R[1:] += best[:R]

            i_max = np.argmax(A_R)
            last[R] = i_max
            best[R] = A_R[i_max]

        # ----------------------------------------------------------------
        # Now find changepoints by iteratively peeling off the last block
        # ----------------------------------------------------------------
        change_points = np.zeros(N, dtype=int)
        i_cp = N
        ind = N
        while True:
            i_cp -= 1
            change_points[i_cp] = ind
            if ind == 0:
                break
            ind = last[ind - 1]
        change_points = change_points[i_cp:]

        return self.mjd[change_points]

#export
class LikelihoodFitness(CountFitness):
    """ Fitness function that uses the full likelihood
    """

    def __init__(self, lc,  p0=0.05, npt=50):
        self.npt = npt
        super().__init__(lc, p0)

    def setup(self):
        df = self.df
        N = self.N

        def liketable(prep):
            return prep.create_table(self.npt)

        self.tables = df.fit.apply(liketable).values

    def __str__(self):
        return f'{self.__class__.__name__}: {self.N} cells,  prior={self.ncp_prior:.1f}'

    def __call__(self, R):

        a, y  = self.tables[R]
        x = np.linspace(*a)
        y = np.zeros(self.npt)
        rv = np.empty(R+1)
        for i in range(R, -1, -1):
            a, yi = self.tables[i]
            xi = np.linspace(*a)
            y += np.interp(x, xi, yi, left=-np.inf, right=-np.inf)
            amax = np.argmax(y)
            rv[i] =y[amax]
        return rv

# Cell
def doc_countfitness( fitness, light_curve_dict, source_name):
    """
    #### {class_name} test with source {source_name}

    Create object: `bbfitter = {class_name}(lc)`

    Object description:   {bbfitter}

    Then `bbfitter({n})` returns the values
        {values}

    Finally, the partition algorithm, 'bbfitter.fit()' returns {cffit}

    """

    lc = light_curve_dict[source_name]
    bbfitter = fitness(lc)
    class_name = bbfitter.name
    n = 10
    values  = np.array(bbfitter(n)).round(1)
    cffit = bbfitter.fit()

    return locals()

# Cell
def get_bb_partition(config, lc, fitness_class=LikelihoodFitness, p0=0.05, key=None, clear=False):

    """Perform Bayesian Block partition of the cells found in a light curve

    - lc : input LightCurve object or DataFrame with fit cells
    - fitness_class

    return edges for partition
    """
    assert issubclass(fitness_class,CountFitness), 'fitness_class wrong'
    if not isinstance(lc, pd.DataFrame):
        lc = lc.dataframe
    assert 'fit' in lc.columns, 'Expect the dataframe to have the Poisson fit object'


    def doit():
        fitness = fitness_class(lc, p0=p0)
        # Now run the astropy Bayesian Blocks code using my version of the 'event' model
        return fitness.fit()

    key = f'BB_edges_' if key is '' else key

    edges = config.cache(key, doit,  description=key if config.verbose>0 else '', overwrite=clear)

    if config.verbose>0:
        print(f'Partitioned {len(lc)} cells into {len(edges)-1} blocks, using {fitness_class.__name__} ' )
    return edges

# Cell
def bb_overplot(config, lc, bb_fit, ax=None, source_name=None, step_name=None, **kwargs):
    """Plot light curve: cell fits with BB overplot
    """
    import matplotlib.pyplot as plt
    colors = kwargs.pop('colors', ('lightblue', 'wheat', 'blue'))
    fig, ax = plt.subplots(1,1, figsize=(12,4)) if not ax else (ax.figure, ax)
    flux_plot(config, lc, ax=ax, colors=colors, source_name=source_name,
              label=step_name+' bins', **kwargs)
    flux_plot(config, bb_fit, ax=ax, step=True,
              label='BB overlay', zorder=10,**kwargs)
    fig.set_facecolor('white')

# Cell
class WtLike(LightCurve):
    """
    """

    def applyBB(self, key=None, clear=False):
        """ Apply the Bayesian Blocks algorithm to partition the current set of cells into blocks,
        then create a new set of cells and fit them

        - key : cache key. None, defaul to not use the cache
        - clear : if True, clear the cache for this key
        """

        self.bb_edges  = get_bb_partition(self.config, self.lc_df,  key=key, clear=clear)

        self.bb_cells = partition_cells(self.config, self.cells, self.bb_edges)
        self.bb_fit = fit_cells(self.config, self.bb_cells, )

    def plot_BB(self, ax=None, **kwargs):
        """Plot the light curve with BB overplot
        """
        import matplotlib.pyplot as plt
        if not hasattr(self, 'bb_cells'):
            self.applyBB()
        figsize = kwargs.pop('figsize', (12,4))
        fignum = kwargs.pop('fignum', 1)
        ts_min = kwargs.pop('ts_min',-1)
        source_name =kwargs.pop('source_name', self.source_name)
        fig, ax = ig, ax = plt.subplots(figsize=figsize, num=fignum) if ax is None else (ax.figure, ax)

#         bb_overplot(self.config, self.lc_df, self.bb_fit, ax=ax, ts_min=ts_min,
#                     source_name=source_name, step_name=self.step_name, **kwargs)
        colors = kwargs.pop('colors', ('lightblue', 'wheat', 'blue') )
        #fig, ax = plt.subplots(1,1, figsize=(12,4)) if not ax else (ax.figure, ax)
        flux_plot(self.config, self.lc_df, ax=ax, colors=colors, source_name=source_name,
                  label=self.step_name+' bins', **kwargs)
        flux_plot(self.config, self.bb_fit, ax=ax, step=True,
                  label='BB overlay', zorder=10,**kwargs)

        fig.set_facecolor('white')
        return fig

    def bb_table(self, **kwargs):
        """ Return a table of fluxes for the BB analysis"""
        return self.flux_table(self.bb_fit, **kwargs)

BBA = WtLike # an alias