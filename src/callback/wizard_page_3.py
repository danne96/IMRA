from tkinter import filedialog as fd

import os

def select_xlsx_output(container, app, res_label, width=50):
	if app.xpr.xlsx_out_dir and os.path.exists(app.xpr.xlsx_out_dir):
		inidir = app.xpr.xlsx_out_dir
	else:
		inidir = app.config["default_output_dir"]
	outdir = fd.askdirectory(parent=container,
							 title="Select output directory",
							 initialdir=inidir)
	if not outdir and app.xpr.xlsx_out_dir:
		outdir = os.path.abspath(app.xpr.xlsx_out_dir)
	else:
		app.xpr.xlsx_out_dir = os.path.abspath(outdir)
	res_text = outdir
	if len(res_text) > width:
		res_text = f"{res_text[:9]}...{res_text[-39:]}"
	res_label.config(text=res_text)

def switch_allow_models(app, var, sel_title, mod_sel):
	'''
	Set whether the selected models will be fitted into the current data.
	'''
	app.xpr.allow_modelling = var.get()
	sel_title.config(state=["disabled", "normal"][app.xpr.allow_modelling])
	for child in mod_sel.contents.winfo_children():
		for gchild in child.winfo_children():
			gchild.winfo_children()[0].config(state=["disabled", "normal"][app.xpr.allow_modelling])
	for child in mod_sel.col_head.winfo_children():
			child.winfo_children()[0].config(state=["disabled", "normal"][app.xpr.allow_modelling])

def switch_plot_data(app, checkvar, dependent_widgets):
	app.xpr.write_plot_data = checkvar.get()
	for dw in dependent_widgets:
		dw.config(state=["disabled", "normal"][checkvar.get()])
	
## Allow/disable XLSX results
def switch_xlsx_output(app, checkvar, dependent_widgets, sec_checkvar, sec_dependent_widgets):
	app.xpr.write_xlsx = checkvar.get()
	for dw in dependent_widgets:
		dw.config(state=["disabled", "normal"][checkvar.get()])
	for dw in sec_dependent_widgets:
		dw.config(state=["disabled", "normal"][checkvar.get() & sec_checkvar.get()])

def update_plot_from(app, stringvar):
	try:
		app.xpr.plot_from = int(stringvar.get())
	except ValueError:
		try:
			stringvar.set(str(round(float(stringvar.get()))))
			app.xpr.plot_from = int(stringvar.get())
		except ValueError:
			stringvar.set(str(app.xpr.plot_from))

## Validate and update the last timepoint for plotting data
def update_plot_to(app, stringvar):
	try:
		app.xpr.plot_to = int(stringvar.get())
	except ValueError:
		try:
			stringvar.set(str(round(float(stringvar.get()))))
			app.xpr.plot_to = int(stringvar.get())
		except ValueError:
			stringvar.set(str(app.xpr.plot_to))

## Validate and update the timestep for plotting data
def update_plot_tstep(app, stringvar):
	try:
		app.xpr.plot_timestep = int(stringvar.get())
	except ValueError:
		try:
			stringvar.set(str(round(float(stringvar.get()))))
			app.xpr.plot_timestep = int(stringvar.get())
		except ValueError:
			stringvar.set(str(app.xpr.plot_timestep))