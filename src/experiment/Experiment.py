import numpy as np
import itertools
import json

from src.experiment.ExperimentEncoder import ExperimentEncoder

from src.session import Session
from src.misc.misc import *

class Experiment:
	def __init__(self,
			     name,
				 desc=None,
				 vars=None,
				 conds=None,
				 path_to_t=None,
				 path_to_DPM=None,
				 blanks=None,
				 raw_data=None,
				 runs=None,
				 processed_data=None,
				 allow_modelling=True,
				 models=None,
				 write_xlsx=False,
				 write_plot_data=False,
				 plot_from=0,
				 plot_to=1000,
				 plot_timestep=1000,
				 xlsx_out_dir="",
				 results=None,
				 *args, **kwargs): # additional arguments allow parsing obsolete properties
								   # that will be removed when a new JSON is saved
		
		self.name = name
		self.desc = desc
		
		self.vars = {"CELL_LINE_BCKG": dict(), "RADIOCHEMICALS": dict(), "SUSPENSIONS": dict(), "CATEGORIES": dict()} if not vars else vars
		self.conds = np.array([[]]) if not conds else conds
		
		self.path_to_t = path_to_t
		self.path_to_DPM = path_to_DPM
		self.blanks = [0, 0] if not blanks else blanks
		
		self.raw_data = {"TIME": [], "DPM": []} if not raw_data else raw_data
		self.runs = [] if not runs else runs
		self.processed_data = dict() if not processed_data else processed_data
		
		self.allow_modelling = allow_modelling
		self.models = {"EXP": False, "EXP_1K": False, "EXP_0K": False} if not models else models
		self.results = dict() if not results else results
					   
		self.write_xlsx = write_xlsx
		self.write_plot_data = write_plot_data
		self.plot_from = plot_from
		self.plot_to = plot_to
		self.plot_timestep = plot_timestep
		self.xlsx_out_dir = xlsx_out_dir

	# Combine data from SELF.VARS to define experimental conditions
	def create_conditions(self):
		conds = [list(self.vars["RADIOCHEMICALS"].keys()),
				 list(self.vars["SUSPENSIONS"].keys())]
		conds += list(self.vars["CATEGORIES"].values())
		conds = list(itertools.product(*conds))
		cond_labs = alphabet_labels(1, len(conds))
		self.conds = dict(zip(cond_labs, conds))	
	
	def compile_runs(self):
		'''	
		Convert raw data (timing and DPM read from files) and run info (read from the wizard) into processed data.

		Creates or updates the "self.processed_data" attribute of a Project class instance.
	    '''
		longest_run = max([run[0] for run in self.runs])
		processed_data = {"T"   : np.full((len(self.runs), longest_run), np.nan),
						  "Y"   : np.full((len(self.runs), longest_run), np.nan),
						  "DPMC": np.full((len(self.runs), longest_run), np.nan), # DPM per million cells
						  "f"   : np.zeros((len(self.runs), 1)),
						  "C0"  : np.zeros((len(self.runs), 1)),
						  "GRP" : []}
		DPM = self.raw_data["DPM"].copy()
		TIME = self.raw_data["TIME"].copy()
		for i, run in enumerate(self.runs):
			this_TIME = TIME[:run[0]]
			processed_data["T"][i, :len(this_TIME)] = this_TIME
			TIME = TIME[run[0]:]
			molrad = self.vars["RADIOCHEMICALS"][self.conds[run[3]][0]]
			dens = self.vars["SUSPENSIONS"][self.conds[run[3]][1]]
			vbar = self.vars["CELL_LINE_BCKG"][self.conds[run[3]][1].split(":")[1]]
			this_DPM = DPM[:run[0]]
			if vbar: # Only calculate tracer concentration when average cell volume is defined
				processed_data["Y"][i, :len(this_DPM)] = np.array(this_DPM) / (run[1] * molrad * dens * vbar) * 1e9
			else: # Otherwise, replace with DPMC
				processed_data["Y"][i, :len(this_DPM)] = np.array(this_DPM) / (dens * run[1]) * 1e6
			processed_data["DPMC"][i, :len(this_DPM)] = np.array(this_DPM) / (dens * run[1]) * 1e6
			DPM = DPM[run[0]:]
			processed_data["f"][i] = vbar * dens * 1e6 / (1 - vbar * dens * 1e6)
			processed_data["C0"][i] = run[2]# * 1e-9
			processed_data["GRP"].append(run[3])
		for k in ["T", "Y", "f", "C0"]:
			processed_data[k] = processed_data[k].tolist()
		self.processed_data = processed_data

	def save(self, app: Session):
		with open(f"{app.config['experiment_dir']}/{self.name}.json", "w") as out:
			json.dump(self.__dict__, out, cls=ExperimentEncoder)
		app.update_experiments()


class Template(Experiment):

	def save(self, app: Session):
		with open(f"{app.config['template_dir']}/{self.name}.json", "w") as out:
			json.dump(self.__dict__, out, cls=ExperimentEncoder)
		app.update_templates()