import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, showerror
import json

from ..session import Session
from ..callback.xpr2xlsx import xpr2xlsx
from ..experiment.Experiment import Experiment, Template
#from imra.experiment.Template import Template
from ..models.models import run_models_for_experiment
from .NewExperimentStart import NewExperimentStart
#from .NewTemplateStart import NewTemplateStart
from .WizardPage1 import WizardPage1
from .WizardPage2 import WizardPage2
from .WizardPage3 import WizardPage3

class NewExperimentWizard(tk.Toplevel):
	def __init__(self, app: Session, is_template=False, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.is_template = is_template
		self.page = NewExperimentStart(self, self.app, is_template)
		self.page.grid(column=0, row=0, sticky=tk.W+tk.N)
	
	def create_new_experiment(self, app: Session, name: str, desc: str, temp: str):
		if not name or not name[0].isalnum():
			showerror(title="Bad Experiment Name",
			 		  message="Please, enter a non-empty name that starts with a letter or a digit.",
					  parent=self)
			return
		
		confirmed = True
		if name in app.xpr_list_names:
			confirmed = askyesno(title="Existing Experiment",
							     message="An experiment with this name already exists. Finishing this wizard "
									     "will overwrite the existing experiment with new data. Continue?")
		if confirmed:
			temp_dict = dict()
			if temp != "--None--":
				with open(f"{app.config['template_dir']}/{temp}.json") as temp_file:
					temp_dict = json.load(temp_file)
					## Remove the 'name' and 'desc' attributes so that
					## they do not clash with the new experiment
					temp_dict.pop("name")
					temp_dict.pop("desc")
				app.xpr = Experiment(name=name, desc=desc, **temp_dict)
			else:
				app.xpr = Experiment(name=name, desc=desc,
						 			 xlsx_out_dir=app.config["default_output_dir"])
			self.load_page_1()
	def create_new_template(self, app: Session, name: str, desc: str):
		if not name or not name[0].isalnum():
			showerror(title="Bad Template Name",
			 		  message="Please, enter a non-empty name that starts with a letter or a digit.",
					  parent=self)
			return
		confirmed = True
		if name in app.tmp_list_names:
			confirmed = askyesno(title="Existing Template",
							 	 message="A template with this name already exists. Finishing this wizard "
							         	 "will overwrite the existing template with new data. Continue?")	
		if confirmed:
			app.xpr = Template(name=name, desc=desc,
						       xlsx_out_dir=app.config["default_output_dir"])
			self.load_page_1()

	def load_page_1(self):
		self.page.destroy()
		self.page = WizardPage1(self, self.app)
		self.page.grid(column=0, row=0, sticky=tk.W+tk.N)
	
	def load_page_2(self, create_conditions=True):
		if create_conditions: # true if coming from page 1, otherwise false
			self.app.xpr.create_conditions()
		self.page.destroy()
		self.page = WizardPage2(self, self.app)
		self.page.grid(column=0, row=0, sticky=tk.W+tk.N)
		
	def load_page_3(self):
		if not self.is_template:
			if not len(self.app.xpr.runs):
				showerror(title="No Runs", parent=self,
			              message="Please, add at least one experimental run.")
				return
			if not all([r[3] for r in self.app.xpr.runs]):
				showerror(title="Missing Conditions", parent=self,
			              message="Please, assing an experimental condition to every run.")
				return
			try:
				self.app.xpr.compile_runs()
			except KeyError: ## Trigerred when an invalid condition is entered.
				showerror(title="Invalid Condition", parent=self,
			              message="A non-existing experimental condition has been assigned to some runs.")
				return
		self.page.destroy()
		self.page = WizardPage3(self, self.app)
		self.page.pack()

	def finish(self):
		if not self.is_template and self.app.xpr.allow_modelling:
			run_models_for_experiment(self.app.xpr, {"maxfev": 500000, "ftol": 1e-15})
		if not self.is_template and self.app.xpr.write_xlsx:
			xpr2xlsx(self.app.xpr)
		self.app.xpr.save(self.app)
		self.destroy()

class ModifyExperimentWizard(NewExperimentWizard):
	def __init__(self, app: Session, is_template=False, *args, **kwargs):
		super(NewExperimentWizard, self).__init__(*args, **kwargs)
		self.app = app
		self.is_template = is_template
		self.page = WizardPage1(self, self.app)
		self.page.grid(column=0, row=0, sticky=tk.W+tk.N)


