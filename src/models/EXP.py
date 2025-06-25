import numpy as np
from scipy.optimize import curve_fit

from ..experiment.Experiment import Experiment

'''
Parsing functions with constant parameters to CURVE_FIT:
	CURVE FIT requires input function in the form of: f(x, p1, ..., pN),
	where 'x' is the independent variable and 'p1' to 'pN' are scalar
	parameters to be optimized. To optimize functions with both variable
	and constant parameters, define a wrapping anonymous functions as
	an input argument for CURVE FIT as follows:
	> potp, pcov = curve_fit(lambda x, p1, ..., pN: f(x, p1, ..., pN, c1, ..., cN), ...)
	Here, 'c1' to 'cN' are the constant parameters that have to be
	explicitly defined elsewhere.
'''

def EXP(t, C0, L, S, K):
	'''
	The exponential growth model chracterizes the functional dependence of the tracer accumulation (Y) on time (t) as:

	Y(t)+ = C0 * L * (1 - exp ** (-t * S)) + K,

	where C0 is the initial tracer concentration, L is the ratio of C0 accumulated in cells at the equilibrium, S is a parameter
	determining the steepness of Y(t) growth, and K is the intercept of Y(t) at t=0.
	'''
	return C0 * L * (1 - np.e ** (-t * S)) + K
def EXP_wrap(t, C0, y0, p0, fit_intercept: bool, *args, **kwargs):
	miss = np.isnan(y0) | np.isnan(t)
	t[miss] = -1
	miss = miss.flatten()
	if fit_intercept:
		popt, pcov = curve_fit(lambda t, *x: EXP(t, C0,
											 	np.array([[L] for L in x[:len(t)]]),
											 	np.array([[S] for S in x[len(t):len(t)*2]]),
											 	np.array([[K] for K in x[len(t)*2:]])).flatten()[~miss],
											 	t, y0.flatten()[~miss], p0=p0, *args, **kwargs)
	else:
		popt, pcov = curve_fit(lambda t, *x: EXP(t, C0,
											 	np.array([[L] for L in x[:len(t)]]),
											 	np.array([[S] for S in x[len(t):len(t)*2]]),
												0).flatten()[~miss],
												t, y0.flatten()[~miss], p0=p0, *args, **kwargs)
	return popt, pcov

def EXP_fit_data(xpr: Experiment, **opt_args):
		popt, pcov = EXP_wrap(np.array(xpr.processed_data["T"]),
							  np.array(xpr.processed_data["C0"]),
							  np.array(xpr.processed_data["Y"]),
							  [1e-3] * len(xpr.runs) * 2 + [0.] * len(xpr.runs), True, **opt_args)
		xpr.results.update({"EXP": {"L": popt[:len(xpr.runs)].tolist(),
									"S": popt[len(xpr.runs):-len(xpr.runs)].tolist(),
									"K": popt[-len(xpr.runs):].tolist(),
									"pcov": pcov.tolist()}})
def EXP_plot_runs(xpr: Experiment, T):
	return EXP(T,	np.array(xpr.processed_data["C0"]),
			  		np.array([[L] for L in xpr.results["EXP"]["L"]]),
					np.array([[S] for S in xpr.results["EXP"]["S"]]),
					np.array([[K] for K in xpr.results["EXP"]["K"]]))

def EXP_1K_fit_data(xpr: Experiment, **opt_args):
		popt, pcov = EXP_wrap(np.array(xpr.processed_data["T"]),
							  np.array(xpr.processed_data["C0"]),
							  np.array(xpr.processed_data["Y"]),
							  [1e-3] * len(xpr.runs) * 2 + [0.], True, **opt_args)
		xpr.results.update({"EXP_1K": {"L": popt[:len(xpr.runs)].tolist(),
									   "S": popt[len(xpr.runs):-1].tolist(),
									   "K": popt[-1],
									   "pcov": pcov.tolist()}})
def EXP_1K_plot_runs(xpr: Experiment, T):
	return EXP(T,	np.array(xpr.processed_data["C0"]),
			  		np.array([[L] for L in xpr.results["EXP_1K"]["L"]]),
					np.array([[S] for S in xpr.results["EXP_1K"]["S"]]),
					xpr.results["EXP_1K"]["K"])

def EXP_0K_fit_data(xpr: Experiment, **opt_args):
		popt, pcov = EXP_wrap(np.array(xpr.processed_data["T"]),
							  np.array(xpr.processed_data["C0"]),
							  np.array(xpr.processed_data["Y"]),
							  [1e-3] * len(xpr.runs) * 2, False, **opt_args)
		xpr.results.update({"EXP_0K": {"L": popt[:len(xpr.runs)].tolist(),
									   "S": popt[len(xpr.runs):].tolist(),
									   "pcov": pcov.tolist()}})
def EXP_0K_plot_runs(xpr: Experiment, T):
	return EXP(T,	np.array(xpr.processed_data["C0"]),
	        		np.array([[L] for L in xpr.results["EXP_0K"]["L"]]),
					np.array([[S] for S in xpr.results["EXP_0K"]["S"]]), 0)