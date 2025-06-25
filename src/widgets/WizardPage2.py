import tkinter as tk
from tkinter import ttk

from ..callback.wizard_page_2 import *
from .ExperimentalRunManagerRow import ExperimentalRunManagerRow
from .ScrollableFrame import ScrollableFrame

class WizardPage2(ttk.Frame):
	def __init__(self, container, app, is_template=False, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		self.app = app
		self.columnconfigure(0, weight=1)
		
		# Row 1: File selector
		fs = ttk.Frame(self)
		fs.grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)
		
		## Select timing data
		t_fname_prompt = ttk.Label(fs, text="Select a TIMING data file:")
		t_fname_prompt.grid(column=0, row=0, sticky=tk.W)
		
		t_fname_btn = ttk.Button(fs, text="Browse")
		t_fname_btn.grid(column=1, row=0, sticky=tk.E)
		if is_template:
			t_fname_btn["state"] = "DISABLED"
		
		t_fname_disp = ttk.Label(fs, text=self.app.xpr.path_to_t, width=50)
		t_fname_disp.grid(column=0, row=1, columnspan=2, sticky=tk.W)
		t_fname_btn.config(command=lambda: select_t_file(self, self.app, t_check, t_fname_disp))
		
		t_check = ttk.Label(fs)
		t_check.grid(column=2, row=1, columnspan=3)
		check_t_file(self.app, t_check)
		
		## Select DPM data
		dpm_fname_prompt = ttk.Label(fs, text="Select a DPM data file:")
		dpm_fname_prompt.grid(column=0, row=2, sticky=tk.W)
		
		dpm_fname_btn = ttk.Button(fs, text="Browse")
		dpm_fname_btn.grid(column=1, row=2, sticky=tk.E)
		
		dpm_blanks_label = ttk.Label(fs, text="Blanks: ")
		dpm_blanks_label.grid(column=2, row=2, sticky=tk.W)
		
		dpm_blanks_for = ttk.Entry(fs, width=3)
		dpm_blanks_for.grid(column=3, row=2, sticky=tk.W, padx=5)
		dpm_blanks_for.insert(0, self.app.xpr.blanks[0])
		
		dpm_blanks_rev = ttk.Entry(fs, width=3)
		dpm_blanks_rev.grid(column=4, row=2, sticky=tk.W, padx=5)
		dpm_blanks_rev.insert(0, self.app.xpr.blanks[1])		
		
		dpm_fname_disp = ttk.Label(fs, text=self.app.xpr.path_to_DPM, width=50)
		dpm_fname_disp.grid(column=0, row=3, columnspan=2, sticky=tk.W)
		dpm_fname_btn.config(command=lambda: select_DPM_file(self, self.app, dpm_check,
															 [int(dpm_blanks_for.get()),
															  int(dpm_blanks_rev.get())],
															 dpm_fname_disp))
		
		dpm_check = ttk.Label(fs)
		dpm_check.grid(column=2, row=3, columnspan=3)
		check_DPM_file(self.app, dpm_check)
		
		# -- A separator --
		sep = ttk.Separator(self, orient="horizontal")
		sep.grid(column=0, row=1, sticky=tk.EW)
		
		# EXPERIMENTAL CONDITION SUMMARY
		cond_title = ttk.Label(self, text="Experimental conditions generated from previously selected variables.", font="TkDefaultFont 10 bold")
		cond_title.grid(column=0, row=2, sticky=tk.W, padx=10, pady=(10, 5))
		## Condition scrollable frame
		cond = ScrollableFrame(self, relief="flat", borderwidth=1.2)
		cond.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)
		cond.canvas.config(height=117, width=480)
		#### Row head
		#rownames = ["Tracer", "Suspension", "Background"] + [f"Category #{i+1}" for i in range(np.array(list(self.app.xpr.conds.values())).shape[1] - 2)]
		rownames = ["Tracer", "Suspension", "Background"] + list(self.app.xpr.vars["CATEGORIES"].keys())
		for name in rownames:
			frm = ttk.Frame(cond.row_head, relief="raised", height=39, width=120, borderwidth=1.2)
			frm.pack_propagate(False)
			frm.pack(fill="x")
			ttk.Label(frm, text=name).pack(side="left", fill="y", padx=(15,5), pady=5)
		cond.create_row_head()
		#### Col head
		for name in self.app.xpr.conds.keys():
			frm = ttk.Frame(cond.col_head, height=39, width=120, relief="raised", borderwidth=1.2)
			frm.pack_propagate(False)
			frm.pack(side="left", fill="y")
			ttk.Label(frm, text=name, font="TkDefaultFont 10 bold").pack(side="left", fill="y", padx=(15, 0))
		cond.create_col_head()
		#### Data
		for i, c in enumerate(self.app.xpr.conds.values()):
			frm1 = ttk.Frame(cond.contents, height=39, width=120)
			frm1.pack_propagate(False)
			frm1.grid(row=0, column=i, sticky=tk.W)
			ttk.Label(frm1, text=c[0]).pack(side="left", fill="y", padx=(15, 0))
			frm2 = ttk.Frame(cond.contents, height=39, width=120)
			frm2.pack_propagate(False)
			frm2.grid(row=1, column=i, sticky=tk.W)
			ttk.Label(frm2, text=c[1].split(":")[0]).pack(side="left", fill="y", padx=(15, 0))
			frm3 = ttk.Frame(cond.contents, height=39, width=120)
			frm3.pack_propagate(False)
			frm3.grid(row=2, column=i, sticky=tk.W)
			ttk.Label(frm3, text=c[1].split(":")[1]).pack(side="left", fill="y", padx=(15, 0))
			for j in range(len(c)-2):
				frm = ttk.Frame(cond.contents, height=39, width=120)
				frm.pack_propagate(False)
				frm.grid(row=j+3, column=i, sticky=tk.W)
				ttk.Label(frm, text=c[j+2]).pack(side="left", fill="y", padx=(15, 0))	
		update_scrollbars(cond)

		# RUN MANAGER
		run_man_title = ttk.Label(self, text="Assign conditions to experimental runs.", font="TkDefaultFont 10 bold")
		run_man_title.grid(column=0, row=4, sticky=tk.W, padx=10, pady=5)
		
		#run_man = ExperimentalRunManager(self, self.app)
		## Create the run manager scrollable frame
		run_man = ScrollableFrame(self, self.app, relief="sunken", borderwidth=1.2)
		run_man.canvas.config(height=250, width=600, highlightthickness=0)
		run_man.grid(column=0, row=5, sticky=tk.W+tk.E, padx=10, pady=5)
		#### Populate the manager with existing runs
		for run in self.app.xpr.runs:
			ExperimentalRunManagerRow(run_man, self.app, *run).pack()
		update_scrollbars(run_man)
		#### Create the column header
		names = ["Run #", "Condition", "Sample\ncount", "Sample vol.\n(µL)", "Tracer conc.\n(nM)", ""]
		widths = [70, 100, 100, 100, 100, 130]
		for name, width in zip(names, widths):
			frm = ttk.Frame(run_man.col_head, width=width, height=49, relief="raised", borderwidth=1.2)
			frm.pack_propagate(False)
			frm.pack(side="left")
			ttk.Label(frm, text=name).pack(side="left", padx=(5, 0))
		run_man.create_col_head()	
		update_scrollbars(run_man)
		
		## Run settings
		set_frame = ttk.Frame(self)
		set_frame.grid(column=0, row=6, sticky=tk.W)
		
		set_lab1 = ttk.Label(set_frame, text="Enter parameters for new runs addedd to the list above:")
		set_lab1.grid(column=0, row=0, columnspan=6, padx=10, sticky=tk.W)
		
		set_samp_count_lab = ttk.Label(set_frame, text="Sample count:")
		set_samp_count_lab.grid(column=0, row=1, padx=(10, 5), sticky=tk.E)
		set_samp_count = ttk.Entry(set_frame, width=5)
		set_samp_count.grid(column=1, row=1)
		set_samp_count.insert(0, 10)
		
		set_samp_vol_lab = ttk.Label(set_frame, text="Sample volume:")
		set_samp_vol_lab.grid(column=0, row=2, padx=(10, 5), sticky=tk.E)
		set_samp_vol = ttk.Entry(set_frame, width=5)
		set_samp_vol.grid(column=1, row=2)
		set_samp_vol.insert(0, 500)
		set_samp_vol_units = ttk.Label(set_frame, text="µL")
		set_samp_vol_units.grid(column=2, row=2)
		
		set_radio_c_lab = ttk.Label(set_frame, text="Radiochemical concentration:")
		set_radio_c_lab.grid(column=0, row=3, padx=(10, 5), sticky=tk.E)
		set_radio_c = ttk.Entry(set_frame, width=5)
		set_radio_c.grid(column=1, row=3)
		set_radio_c.insert(0, 2.0)
		set_radio_c_units = ttk.Label(set_frame, text="nM")
		set_radio_c_units.grid(column=2, row=3)
		
		set_runs_to_add_lab = ttk.Label(set_frame, text="Amount of runs to add:")
		set_runs_to_add_lab.grid(column=3, row=1, padx=(10, 5), sticky=tk.E)
		set_runs_to_add = ttk.Entry(set_frame, width=5)
		set_runs_to_add.grid(column=4, row=1)
		set_runs_to_add.insert(0, 1)

		set_add_runs_btn = ttk.Button(set_frame, text="Add runs")
		'''
		set_add_runs_btn.config(command=lambda: add_rows_to_run_manager(run_man, self.app,
																	   [ExperimentalRunManagerRow(run_man, self.app,
																								  int(set_samp_count.get()),
																								  float(set_samp_vol.get()),
																								  float(set_radio_c.get())) for _ in range(int(set_runs_to_add.get()))]))
		'''
		set_add_runs_btn.config(command=lambda: add_rows_to_run_manager_button(run_man, self.app, set_samp_count,
																		       set_samp_vol, set_radio_c, set_runs_to_add))
		set_add_runs_btn.grid(column=4, row=2, padx=5, pady=5, sticky=tk.W)
		
		# << NAVIGATION >>
		nav = ttk.Frame(self)
		nav.grid(column=0, row=7, padx=10, pady=10, sticky=tk.W+tk.E+tk.S)
		nav.grid_columnconfigure(0, weight=1)
		nav.grid_columnconfigure(1, weight=1)

		prev_btn = ttk.Button(nav, text="<< Previous",
							  command=self.master.load_page_1)
		prev_btn.grid(column=0, row=0, sticky=tk.W)
		next_btn = ttk.Button(nav, text="Next >>",
							  command=self.master.load_page_3)
		next_btn.grid(column=1, row=0, sticky=tk.E)

