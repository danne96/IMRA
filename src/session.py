import json
import os

class Session:
	'''
	A 'Session' instance is created when the program starts. It is used to contain the current experiment, template,
	and configuration and make them accessible to widgets or callback methods.
	'''
	def __init__(self):
		## Load program configuration 
		with open("config.json") as config:
			self.config = json.load(config)
		
		## Load all existing experiments
		self.update_experiments()
		
		## Load all existing experiment templates
		self.update_templates()
		
		## Load available radio sheets
		self.radio_compounds = dict()
		for sheet in [sheet for sheet in os.listdir(self.config["radio_sheet_dir"]) if os.path.splitext(sheet)[-1] == ".xlsx"]:
			compound = "-".join(sheet.split()[0].split("-")[:-1])
			if compound not in self.radio_compounds.keys():
				self.radio_compounds.update({compound: []})
			batch = sheet.split()[0].split("-")[-1]
			self.radio_compounds[compound].append((batch, sheet))
	
	def update_experiments(self):
		self.xpr_list = os.listdir(self.config["experiment_dir"])
		self.xpr_list_names = sorted([os.path.splitext(_)[0] for _ in self.xpr_list if _[0].isalnum()])
	
	def update_templates(self):
		self.tmp_list = os.listdir(self.config["template_dir"])
		self.tmp_list_names = sorted([os.path.splitext(_)[0] for _ in self.tmp_list if _[0].isalnum()])	
