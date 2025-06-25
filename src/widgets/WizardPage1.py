import tkinter as tk
from tkinter import ttk

from ..callback.wizard_page_1 import *
from .ScrollableFrame import ScrollableFrame
from ..misc.misc import CELL_LINE_VBAR

class WizardPage1(ttk.Frame):
	def __init__(self, container, app, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		self.app = app
		
		#    CELL LINES
		##   Row 0 (Section title)
		###  Title
		cl_title = ttk.Label(self, text="Enter cell suspensions (and their backgrounds) used in the experiment.", font="TkDefautltFont 10 bold")
		cl_title.grid(column=0, row=0, columnspan=8, padx=(10,0), pady=(10,5), sticky=tk.W)		
		##   Row 1 (Suspension density: Widgets)
		###  "Suspension" label
		sd_name_label = ttk.Label(self, text="Suspension:")
		sd_name_label.grid(column=0, row=1, padx=(10, 5), pady=(5, 10), sticky=tk.W)
		###  "Suspension" entry
		sd_name = ttk.Entry(self, width=10)
		sd_name.grid(column=1, row=1, columnspan=3, padx=5, sticky=tk.W)
		###  "Density" label
		sd_dens_label = ttk.Label(self, text="Density:")
		sd_dens_label.grid(column=4, row=1, sticky=tk.W)
		###  "Density" entry
		sd_dens = ttk.Entry(self, width=10)
		sd_dens.grid(column=5, row=1, padx=(5, 0), sticky=tk.W)
		###  "Density" units
		sd_dens_units = ttk.Label(self, text="1/mL")
		sd_dens_units.grid(column=6, row=1, padx=5, sticky=tk.W)
		##   Row 2 (Pre-defined CL: Subsection title)
		###  Title
		cl_title = ttk.Label(self, text="Select a pre-defined cell line or enter your own")#text="Select a pre-defined cell line background.")
		cl_title.grid(column=0, row=2, columnspan=8, padx=(10,0), pady=(10,5), sticky=tk.W)
		##   Row 3 (Pre-defined CL: Widgets)
		###  "Background" label
		cl_combo_label = ttk.Label(self, text="Cell line:")
		cl_combo_label.grid(column=0, row=3, padx=(10,5), pady=5, sticky=tk.W)
		###  "Background" combobox
		cl_combo = ttk.Combobox(self, width=10, values=list(CELL_LINE_VBAR.keys()))
		cl_combo.grid(column=1, row=3, padx=5, columnspan=3, sticky=tk.W)
		cl_combo.bind("<<ComboboxSelected>>", lambda e: display_predefined_cell_volume(cl_combo, cl_volume))
		###  "Volume" label
		cl_volume_label = ttk.Label(self, text="Volume:")
		cl_volume_label.grid(column=4, row=3, sticky=tk.W)
		###  "Volume" entry
		cl_volume = ttk.Entry(self, width=10)#, state="disabled", foreground="black")
		cl_volume.grid(column=5, row=3, padx=(5,0), sticky=tk.W)
		###  "Volume" units
		cl_predef_volume_units = ttk.Label(self, text="m^3")
		cl_predef_volume_units.grid(column=6, row=3, padx=5, sticky=tk.W)
		###  "Add" button
		cl_predef_btn = ttk.Button(self, text="Add",
								   command=lambda: add_cell_line_to_counter_button(cl_counter, self.app, sd_name, cl_combo, sd_dens, cl_volume))
		cl_predef_btn.grid(column=7, row=3, padx=(5, 10), sticky=tk.E)
		cl_note = ttk.Label(self, text="NOTE: Enter 0 for unspecified/unknown volume")
		cl_note.grid(column=4, row=4, columnspan=4, padx=( 0, 5), pady=5, sticky=tk.W)
		##   Row 6 (CL Counter)
		###  Scrollable frame
		cl_counter = ScrollableFrame(self, borderwidth=1.2, relief="sunken", vertical_increment=True)
		#cl_counter = ScrollableFrame(self, borderwidth=1.5, vertical_increment=True)
		cl_counter.canvas.config(height=100, width=670)
		cl_counter.grid(column=0, row=6, columnspan=8, padx=10, pady=10, sticky=tk.W+tk.E)
		#### Prepare container frames for column heading labels
		frames = [ttk.Frame(cl_counter.col_head, width=fw, height=39, relief="raised", borderwidth=1.5) for fw in [180, 180, 180, 130]]
		for i, frame in enumerate(frames):
			frame.grid(column=i, row=0, sticky=tk.W)
			frame.pack_propagate(False)
		#### Insert column heading labels
		ttk.Label(frames[0], text="Suspension").pack(side="left", padx=(15,0))
		ttk.Label(frames[1], text="Density × mL").pack(side="left", padx=(15,0))
		ttk.Label(frames[2], text="Cell Volume / m^3").pack(side="left", padx=(15,0))
		cl_counter.create_col_head()
		#### Populate the counter with existing project data
		for key, dens in self.app.xpr.vars["SUSPENSIONS"].items():
			susp = key.split(":")[0]
			bckg = key.split(":")[1]
			vbar = self.app.xpr.vars["CELL_LINE_BCKG"][bckg]
			add_cell_line_to_counter(cl_counter, app, susp, bckg, dens, vbar, update_xpr=False)	
		
		# ---RADIOCHEMICALS---
		##   Row 7 (Section title)
		###  Title
		ra_title = ttk.Label(self, text="Enter radiochemicals (tracers) used in the experiment.", font="TkDefaultFont 10 bold")
		ra_title.grid(column=0, row=7, columnspan=8, padx=(10, 5), pady=(10, 5), sticky=tk.W)		
		##   Row 8 (Pre-defined RA: Subsection title)
		###  Title
		ra_subtitle = ttk.Label(self, text="Select from the radiosheet database or enter your own")
		ra_subtitle.grid(column=0, row=8, columnspan=8, padx=(10, 5), pady=5, sticky=tk.W)
		##   Row 9 (Pre-defined RA: Widgets)
		###  "Tracer" label
		ra_comp_combo_label = ttk.Label(self, text="Tracer:")
		ra_comp_combo_label.grid(column=0, row=9, padx=(10, 5), sticky=tk.W)
		###  "Tracer" combobox
		ra_comp_combo = ttk.Combobox(self, values=sorted(app.radio_compounds.keys()), width=8)
		ra_comp_combo.grid(column=1, row=9, padx=5, pady=5, sticky=tk.W)
		ra_comp_combo.bind("<<ComboboxSelected>>",
						   lambda e: display_radio_compound_batches(app, ra_comp_combo, ra_batch_combo, ra_molrad_value))
		###  "Batch" label
		ra_batch_combo_label = ttk.Label(self, text="Batch:")
		ra_batch_combo_label.grid(column=2, row=9, padx=5, sticky=tk.W)
		###  "Batch" combobox
		ra_batch_combo = ttk.Combobox(self, values=[], width=5)
		ra_batch_combo.grid(column=3, row=9, padx=5, sticky=tk.W)
		ra_batch_combo.bind("<<ComboboxSelected>>",
							lambda e: display_predef_molar_radioactivity(app, ra_comp_combo, ra_batch_combo, ra_molrad_value))
		###  "Mol. rad." label
		ra_molrad_label = ttk.Label(self, text="mol. rad.:")
		ra_molrad_label.grid(column=4, row=9, padx=5, sticky=tk.W)
		###  "Mol. rad." entry
		ra_molrad_value = ttk.Entry(self, width=10)#, state="disabled", foreground="black")
		ra_molrad_value.grid(column=5, row=9, padx=(5, 0), sticky=tk.W)
		###  "Mol. rad." units
		ra_predef_molrad_units = ttk.Label(self, text="DPM/mol")
		ra_predef_molrad_units.grid(column=6, row=9, padx=5, sticky=tk.W)
		###  "Add" button
		ra_predef_btn = ttk.Button(self, text="Add",
								   command=lambda: add_radiochemical_to_counter_button(ra_counter, self.app, ra_comp_combo,
																				ra_batch_combo, ra_molrad_value))
		ra_predef_btn.grid(column=7, row=9, padx=(5, 10), sticky=tk.E)											   
		##   Row 12 (Counter)
		###  Scrollable frame
		ra_counter = ScrollableFrame(self, borderwidth=1.2, relief="sunken", vertical_increment=True)
		ra_counter.canvas.config(height=100, width=670)
		ra_counter.grid(column=0, row=12, columnspan=8, padx=10, pady=10, sticky=tk.W+tk.E)
		#### Prepare container frames for column heading labels
		frames = [ttk.Frame(ra_counter.col_head, width=fw, height=39, relief="raised", borderwidth=1.5) for fw in [270, 270, 130]]
		for i, frame in enumerate(frames):
			frame.grid(column=i, row=0, sticky=tk.W)
			frame.pack_propagate(False)
		#### Insert column heading labels
		ttk.Label(frames[0], text="Tracer").pack(side="left", padx=(15,0))
		ttk.Label(frames[1], text="Molar Radioactivity / (DPM/mol)").pack(side="left", padx=(15,0))
		ra_counter.create_col_head()
		#### Populate the counter with existing project data
		for name, value in self.app.xpr.vars["RADIOCHEMICALS"].items():
			add_radiochemical_to_counter(ra_counter, self.app, name, value, update_xpr=False)				
		
		# ---TREATMENTS et al.---
		##   Row 13 (Section title)
		###  Title
		tr_title = ttk.Label(self, text="Enter additional categorical variables.", font="TkDefaultFont 10 bold")
		tr_title.grid(column=0, row=13, columnspan=8, padx=10, pady=(10, 5), sticky=tk.W)
		##   Row 14 (Widgets)
		ttk.Label(self, text="Category:").grid(column=0, row=14, padx=(10, 5), pady=5, sticky=tk.W)
		cat_name = ttk.Entry(self, width=20)
		cat_name.grid(column=1, row=14, columnspan=3, padx=(10, 5), pady=5, sticky=tk.W)
		ttk.Label(self, text="Value:").grid(column=4, row=14, padx=(10, 5), pady=5, sticky=tk.W)
		val_name = ttk.Entry(self, width=20)
		val_name.grid(column=5, row=14, columnspan=4, padx=(10, 5), pady=5, sticky=tk.W)
		cat_btn = ttk.Button(self, text="Add", command=lambda: add_category_to_counter_button(tr_counter, self.app, cat_name, val_name))
		cat_btn.grid(column=7, row=14, padx=10, sticky=tk.E, pady=5)
		## Row 15 (Counter)
		tr_counter = ScrollableFrame(self, borderwidth=1.2, relief="sunken", vertical_increment=True)
		tr_counter.canvas.config(height=100, width=670, highlightthickness=0)		
		tr_counter.grid(column=0, row=15, columnspan=8, padx=10, pady=10, sticky=tk.W+tk.E)
		#### Prepare container frames for column heading labels
		frames = [ttk.Frame(tr_counter.col_head, width=fw, height=39, relief="raised", borderwidth=1.5) for fw in [270, 270, 130]]
		for i, frame in enumerate(frames):
			frame.grid(column=i, row=0, sticky=tk.W)
			frame.pack_propagate(False)
		#### Insert column heading labels
		ttk.Label(frames[0], text="Category").pack(side="left", padx=(15,0))
		ttk.Label(frames[1], text="Value").pack(side="left", padx=(15,0))
		tr_counter.create_col_head()
		#### Populate the counter with existing project data
		for cat in self.app.xpr.vars["CATEGORIES"]:
			for val in self.app.xpr.vars["CATEGORIES"][cat]:
				add_category_to_counter(tr_counter, self.app, cat, val, update_xpr=False)
		
		# << NAVIGATION >>
		## Row 18
		nextbtn = ttk.Button(self, text="Next >>")
		nextbtn.grid(column=7, row=18, padx=10, pady=10, sticky=tk.E)
		nextbtn.config(command=lambda: self.master.load_page_2())
		
	
	# Fill a counter within the frame with variables already stored in
	# the project; use when modifying an existing project or coming back
	# to the page 1 of the wizard 
	def fill_counter_from_project(self, counter, var):
		for key, value in self.app.xpr.vars[var].items():
			counter.add_to(self.app, var, key, value, update_xpr=False)

