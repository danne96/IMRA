import tkinter as tk
from tkinter import ttk

from ..callback.update_scrollbars import update_scrollbars
from ..callback.wizard_page_3 import *
from ..models.models import MODELS
from .ModelSelectRow import ModelSelectRow
from .ScrollableFrame import ScrollableFrame

class WizardPage3(ttk.Frame):
	def __init__(self, container, app, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		self.app = app
		
		# Modelling
		mod = ttk.Frame(self)
		mod.grid(column=0, row=0, sticky=tk.W, padx=10)
		## Title
		mod_tit = ttk.Label(mod, text="Select model(s) to fit to the experimental data", font="TkDefaultFont 10 bold")
		mod_tit.grid(column=0, row=0, sticky=tk.W)
		## Allow modelling
		allow_mod_var = tk.IntVar()
		if self.app.xpr.allow_modelling:
			allow_mod_var.set(1)
		allow_mod = ttk.Checkbutton(mod, text="Allow modelling (feel free to uncheck when modifying an existing experiment to skip calculations)",
								    variable=allow_mod_var,
									command=lambda: switch_allow_models(self.app, allow_mod_var, mod_sel_tit, mod_sel))
		allow_mod.grid(column=0, row=1, sticky=tk.W)
		
		## Select models
		mod_sel_tit = ttk.Label(mod, text="Pick from the list below.")
		mod_sel_tit.grid(column=0, row=2, sticky=tk.W)
		mod_sel = ScrollableFrame(mod, relief="sunken", borderwidth=1.2, vertical_increment=True, horizontal_increment=True)
		mod_sel.canvas.config(width=700)
		mod_sel.grid(column=0, row=3, sticky=tk.W)
		#### Create column headings
		widths = [125, 575]
		names = ["Name", "Description"]
		for width, name in zip (widths, names):
			fr = ttk.Frame(mod_sel.col_head, relief="raised", borderwidth=1.2, width=width, height=49)
			fr.pack_propagate(False)
			fr.pack(side="left")
			ttk.Label(fr, text=name).pack(side="left", padx=(10, 0))
		mod_sel.create_col_head()
		#### Add selectable models
		model_rows = []
		for model in self.app.xpr.models.keys():
			ModelSelectRow(mod_sel.contents, self.app, model, MODELS[model][0], MODELS[model][1]).pack(fill="x")
		update_scrollbars(mod_sel)

		if not self.app.xpr.allow_modelling:
			mod_sel_tit.config(state="disabled")
			for child in mod_sel.contents.winfo_children():
				for gchild in child.winfo_children():
					gchild.winfo_children()[0].config(state="disabled")
			for child in mod_sel.col_head.winfo_children():
				child.winfo_children()[0].config(state="disabled")
		
		# Output
		out = ttk.Frame(self)
		out.grid(column=0, row=1, sticky=tk.W, padx=10)
		## Title
		out_tit = ttk.Label(out, text="Select options for project output", font="TkDefaultFont 10 bold")
		out_tit.grid(column=0, row=0, sticky=tk.W, padx=5)
		## XLSX
		write_xlsx = tk.IntVar()
		xlsx_check = ttk.Checkbutton(out, text="Write results into a spreadsheet", variable=write_xlsx)
		xlsx_check.grid(column=0, row=1, sticky=tk.W, padx=5)
		#### Ploting data
		write_plot_data = tk.IntVar()
		plot_data_check = ttk.Checkbutton(out, text="Include data for plotting", variable=write_plot_data)
		plot_data_check.grid(column=1, row=1, columnspan=6, sticky=tk.W, padx=5)
		###### Plot from
		plot_from_lab = ttk.Label(out, text="Plot from")
		plot_from_lab.grid(column=1, row=2, sticky=tk.W, padx=5)
		self.plot_from_var = tk.StringVar(value=self.app.xpr.plot_from)
		plot_from_entry = ttk.Entry(out, width=5, textvariable=self.plot_from_var)
		plot_from_entry.bind("<FocusOut>", lambda e: update_plot_from(self.app, self.plot_from_var))
		plot_from_entry.grid(column=2, row=2, sticky=tk.W, padx=(0, 5))
		plot_from_unit = ttk.Label(out, text="s")
		plot_from_unit.grid(column=3, row=2, sticky=tk.W, padx=(0, 5))
		###### Plot to
		plot_to_lab = ttk.Label(out, text="to")
		plot_to_lab.grid(column=4, row=2, sticky=tk.W, padx=5)
		self.plot_to_var = tk.StringVar(value=self.app.xpr.plot_to)
		plot_to_entry = ttk.Entry(out, width=5, textvariable=self.plot_to_var)
		plot_to_entry.bind("<FocusOut>", lambda e: update_plot_to(self.app, self.plot_to_var))
		plot_to_entry.grid(column=5, row=2, sticky=tk.W, padx=(0, 5))
		plot_to_unit = ttk.Label(out, text="s")
		plot_to_unit.grid(column=6, row=2, sticky=tk.W, padx=(0, 5))
		###### Plot timestep
		plot_tstep_lab = ttk.Label(out, text="with a timestep of")
		plot_tstep_lab.grid(column=1, row=3, columnspan=4, sticky=tk.W, padx=5)
		self.plot_tstep_var = tk.StringVar(value=self.app.xpr.plot_timestep)
		plot_tstep_entry = ttk.Entry(out, width=5, textvariable=self.plot_tstep_var)
		plot_tstep_entry.bind("<FocusOut>", lambda e: update_plot_tstep(self.app, self.plot_tstep_var))
		plot_tstep_entry.grid(column=5, row=3, sticky=tk.W, padx=(0, 5))
		plot_tstep_unit = ttk.Label(out, text="ms")
		plot_tstep_unit.grid(column=6, row=3, sticky=tk.W, padx=(0, 5))
		
		xlsx_out_dir_lab = ttk.Label(out, text="Select the output directory:")
		xlsx_out_dir_lab.grid(column=0, row=4, sticky=tk.W, padx=5)
		xlsx_out_dir_btn = ttk.Button(out, text="Browse",
									  command=lambda: select_xlsx_output(self, self.app, xlsx_out_dir_res))
		xlsx_out_dir_btn.grid(column=1, row=4, columnspan=7, sticky=tk.W, padx=5)
		xlsx_out_dir_res = ttk.Label(out, text=os.path.abspath(self.app.xpr.xlsx_out_dir), width=50)
		xlsx_out_dir_res.grid(column=0, row=5, columnspan=7, sticky=tk.W, padx=5)
		
		xlsx_widgets = [plot_data_check, xlsx_out_dir_lab, xlsx_out_dir_btn, xlsx_out_dir_res]
		plot_data_widgets = [plot_from_lab, plot_from_entry, plot_from_unit, plot_to_lab, plot_to_entry,
							 plot_to_unit, plot_tstep_lab, plot_tstep_entry, plot_tstep_unit]
							 
		xlsx_check.config(command=lambda: switch_xlsx_output(self.app, write_xlsx, xlsx_widgets, write_plot_data, plot_data_widgets))
		plot_data_check.config(command=lambda: switch_plot_data(self.app, write_plot_data, plot_data_widgets))
		
		if not self.app.xpr.write_xlsx:
			for widget in xlsx_widgets + plot_data_widgets:
				widget.config(state="disabled")			
		else:
			write_xlsx.set(1)
			if not self.app.xpr.write_plot_data:
				for widget in plot_data_widgets:
					widget.config(state="disabled")			
		if self.app.xpr.write_plot_data:
			write_plot_data.set(1)
		
		
		# << NAVIGATION >>
		nav = ttk.Frame(self)
		nav.grid(column=0, row=2, sticky=tk.W+tk.E, padx=10, pady=10)
		nav.grid_columnconfigure(0, weight=1)
		nav.grid_columnconfigure(1, weight=1)
		prev_btn = ttk.Button(nav, text="<< Previous",
							  command=lambda: self.master.load_page_2(create_conditions=False))
		prev_btn.grid(column=0, row=0, sticky=tk.W)
		fin_btn = ttk.Button(nav, text="Finish", command=lambda: self.master.finish())
		s = ttk.Style()
		s.configure("Finish.TButton", weight="bold")
		fin_btn.config(style="Finish.TButton")
		fin_btn.grid(column=1, row=0, sticky=tk.E)

