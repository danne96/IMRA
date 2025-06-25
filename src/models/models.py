from .EXP import *

'''
A comprehensive list of models and their associated methods.
'''
MODELS = {
	"EXP":		["Exp",		"EXPONENTIAL MODEL: The tracer accumulation (Y) is a function of time (t), applied\n"
		  					"tracer concentration (c0 - a constant), accumulation curve limit (L) and steepness (S),\n"
							"as well as its intercept at t=0 (K). The model estimates L, S, and K for each run.\n"
							"Y(t) = c0 * L * [1 - e^(-t * S)] + K",
				EXP_fit_data, EXP_plot_runs],
	 "EXP_1K":	["Exp_1K",	"An exponential model (see above) that fits a single value of K into the whole dataset,\n"
			 				"making the intercepts of all Y(t) curves equal.",
				EXP_1K_fit_data, EXP_1K_plot_runs],
	 "EXP_0K":	["Exp_0K",	"An exponential model (see above) with K = 0 for each run, i.e.\n"
			   				"Y(t) = c0 * L * [1 - e^(-t * S)]",
				EXP_0K_fit_data, EXP_0K_plot_runs]
}

def run_models_for_experiment(xpr: Experiment, opt_args):
	for m in xpr.models.keys():
		if xpr.models[m]:
			MODELS[m][2](xpr, **opt_args)
