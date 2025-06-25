import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from natsort import natsorted
import pandas as pd

from ..callback.update_scrollbars import update_scrollbars
from ..misc.misc import CELL_LINE_VBAR
from ..session import Session

## Display the pre-defined cell volume in an entry.
def display_predefined_cell_volume(combobox, entry):
	selected_cl = combobox.get()
	#entry.config(state="enabled")
	entry.delete(0, tk.END)
	entry.insert(0, CELL_LINE_VBAR[selected_cl])
	#entry.config(state="disabled")

## Display relevant batches to the selected radio compound.
def display_radio_compound_batches(app, compound_combo, batch_combo, entry):
	compound = compound_combo.get()
	batch_tups = app.radio_compounds[compound]
	batches = natsorted([tup[0] for tup in batch_tups])
	batches.reverse()
	batch_combo.config(values=batches)
	batch_combo.set(batches[0])
	display_predef_molar_radioactivity(app, compound_combo, batch_combo, entry)

def check_and_get_values_for_counter(counter, strings=None, numerals=None, str_messages=None, num_messages=None):
	str_values = []
	num_values = []
	if strings:
		for i, s in enumerate(strings):
			sval = s.get()
			if sval:
				str_values.append(sval)
			else:
				showerror(title="Error", parent=counter.master.master,
			  		      message=str_messages[i])
				return
	if numerals:
		for i, n in enumerate(numerals):
			try:
				num_values.append(float(n.get()))
			except ValueError:
				showerror(title="Error", parent=counter.master.master,
			  			  message=num_messages[i])
				return

	return str_values, num_values

def add_cell_line_to_counter(counter, app: Session, susp, bckg, dens, vbar, update_xpr=True):
	'''
	Add a new cell line frame to the counter or update an existing one
	'''
	susp_labels = [frame.winfo_children()[0].winfo_children()[0].cget("text") for frame in counter.contents.winfo_children()]
	if f"{susp}:{bckg}" not in susp_labels:
		frame = ttk.Frame(counter.contents) # one frame to keep 'em all
		subs = [ttk.Frame(frame, width=fw, height=39) for fw in [180, 180, 180, 130]]
		for i, sub in enumerate(subs):
			sub.grid(column=i, row=0, sticky=tk.W)
			sub.pack_propagate(False)
		ttk.Label(subs[0], text=f"{susp}:{bckg}").pack(side="left", padx=15, fill="y")
		ttk.Label(subs[1], text=f"{dens:6g}").pack(side="right", padx=15, fill="y")
		ttk.Label(subs[2], text=f"{vbar:6g}").pack(side="right", padx=15, fill="y")
		ttk.Button(subs[3], text="Delete", command=lambda: remove_cell_line_from_counter(frame, counter, app)).pack(side="left", padx=(15,0))
		frame.pack(fill="x")
	else:
		ndx = susp_labels.index(f"{susp}:{bckg}")
		frame = counter.contents.winfo_children()[ndx]
		dens_lab = frame.winfo_children()[1].winfo_children()[0]
		dens_lab.config(text=f"{dens:6g}")
	#### The block below executes if the user changes the average cell volume of an existing cell line
	if bckg in app.xpr.vars["CELL_LINE_BCKG"].keys() and app.xpr.vars["CELL_LINE_BCKG"][bckg] != vbar:
		for i, frame in enumerate(counter.contents.winfo_children()):
			if list(app.xpr.vars["SUSPENSIONS"].keys())[i].split(":")[1] == bckg:
				vbar_lab = frame.winfo_children()[2].winfo_children()[0]
				vbar_lab.config(text=f"{vbar:6g}")
		
	if update_xpr:
		app.xpr.vars["SUSPENSIONS"].update({f"{susp}:{bckg}": dens})
		app.xpr.vars["CELL_LINE_BCKG"].update({bckg:vbar})
	
	update_scrollbars(counter)
def add_cell_line_to_counter_button(counter, app: Session, susp_entry: ttk.Entry, cl_combo: ttk.Combobox, dens_entry: ttk.Entry, vol_entry: ttk.Entry):
	'''
	Read the user-provided data on cell suspension and cell line background. Perform a check and if successful, add these data to the
	counter using the 'add_cell_line_to_counter' function. Triggered when the user presses the corresponding 'Add' button.
	'''
	try:
		[susp, bckg], [dens, vbar] = check_and_get_values_for_counter(counter, [susp_entry, cl_combo], [dens_entry, vol_entry],
																  	  ["Please, enter an indentifier for your cell suspension.",
																	   "Please, specify the cell line."],
															      	  ["The entered cell suspension density is not a valid floating-point number.",
					   												   "The entered cell volume is not a valid floating-point number."])
	except TypeError:
		return
	if dens <= 0:
		showerror(title="Error", parent=counter.master.master,
				  message="The cell suspension density must be greater than zero.")
		return
	if vbar < 0:
		showerror(title="Error", parent=counter.master.master,
			 	  message="The cell volume must be non-negative.")
		return
	add_cell_line_to_counter(counter, app, susp, bckg, dens, vbar) 
def remove_cell_line_from_counter(frame, counter, app):
	'''
	Have a line in the cell counter removed when user presses the 'Delete' button.
	'''
	app.xpr.vars["SUSPENSIONS"].pop(frame.winfo_children()[0].winfo_children()[0].cget("text"))
	frame.pack_forget()
	frame.destroy()
	update_scrollbars(counter)
	
## Add a radiochemical frame to the counter & update the project
def add_radiochemical_to_counter(counter, app: Session, name, value, update_xpr=True):
	'''
	Add a frame that contains the name, batch, and molar radioactivity of a tracer to the counter.
	'''
	name_labs = [frame.winfo_children()[0].winfo_children()[0].cget("text") for frame in counter.contents.winfo_children()]
	if name not in name_labs:
		frame = ttk.Frame(counter.contents)
		subs = [ttk.Frame(frame, width=fw, height=39) for fw in [270, 270, 130]]
		for i, sub in enumerate(subs):
			sub.grid(column=i, row=0, sticky=tk.W)
			sub.pack_propagate(False)
		ttk.Label(subs[0], text=name).pack(side="left", padx=(15,0), fill="y")
		ttk.Label(subs[1], text=f"{value:6g}").pack(side="right", padx=15, fill="y")
		ttk.Button(subs[2], text="Delete", command=lambda: remove_radiochemical_from_counter(frame, counter, app)).pack(side="left", padx=(15,0))
		frame.pack(fill="x")
	else:
		ndx = name_labs.index(name)
		frame = counter.contents.winfo_children()[ndx]
		value_lab = frame.winfo_children()[1].winfo_children()[0]
		value_lab.config(text=f"{value:6g}")
	if update_xpr:
		app.xpr.vars["RADIOCHEMICALS"].update({name: value})
	
	update_scrollbars(counter)
def add_radiochemical_to_counter_button(counter, app: Session, tracer_combo: ttk.Entry, batch_combo: ttk.Combobox, value_entry: ttk.Entry):
	'''
	Read the user-provided data on a radioactive tracer. Perform a check and if successful, add these data to the
	counter using the 'add_radiochemical_to_counter' function. Triggered when the user presses the corresponding 'Add' button.	
	'''
	try:
		[tracer, batch], [value] = check_and_get_values_for_counter(counter, [tracer_combo, batch_combo], [value_entry],
															        ["Please, select or enter the name of the radio-labelled tracer.",
																	 "Please, select or enter the tracer batch."],
																	["The entered molar radioactivity is not a valid floating-point number."])
	except TypeError:
		return
	if value <= 0:
		showerror(title="Error", parent=counter.master.master,
				  message="The molar radioactivity must be greater than zero.")
		return
	add_radiochemical_to_counter(counter, app, f"{tracer}:{batch}", value)
def remove_radiochemical_from_counter(frame, counter, app):
	app.xpr.vars["RADIOCHEMICALS"].pop(frame.winfo_children()[0].winfo_children()[0].cget("text"))
	frame.pack_forget()
	frame.destroy()
	update_scrollbars(counter)
	
def add_category_to_counter(counter, app, cat, val, update_xpr=True):
	labs = [(frame.winfo_children()[0].winfo_children()[0].cget("text"), frame.winfo_children()[1].winfo_children()[0].cget("text")) for frame in counter.contents.winfo_children()]
	if (cat, val) not in labs:
		frame = ttk.Frame(counter.contents)
		subs = [ttk.Frame(frame, width=fw, height=39) for fw in [270, 270, 130]]
		for i, sub in enumerate(subs):
			sub.grid(column=i, row=0, sticky=tk.W)
			sub.pack_propagate(False)
		ttk.Label(subs[0], text=cat).pack(side="left", padx=(15,0), fill="y")
		ttk.Label(subs[1], text=val).pack(side="left", padx=(15,0), fill="y")
		ttk.Button(subs[2], text="Delete", command=lambda: remove_category_from_counter(frame, counter, app)).pack(side="left", padx=(15,0))
		frame.pack(fill="x")

		if update_xpr:
			if cat not in app.xpr.vars["CATEGORIES"].keys():
				app.xpr.vars["CATEGORIES"].update({cat: []})
			app.xpr.vars["CATEGORIES"][cat].append(val)
			
	update_scrollbars(counter)
def add_category_to_counter_button(counter, app: Session, cat_entry: ttk.Entry, val_entry: ttk.Entry):
	try:
		[cat, val], _ = check_and_get_values_for_counter(counter, [cat_entry, val_entry], None,
												  	 	 ["Please, enter a category name.",
				 									  	  "Please, enter a category value."])
	except TypeError:
		return
	add_category_to_counter(counter, app, cat, val)
def remove_category_from_counter(frame, counter, app):
	cat = frame.winfo_children()[0].winfo_children()[0].cget("text")
	val = frame.winfo_children()[1].winfo_children()[0].cget("text")
	ndx = app.xpr.vars["CATEGORIES"][cat].index(val)
	app.xpr.vars["CATEGORIES"][cat].pop(ndx)
	if not app.xpr.vars["CATEGORIES"][cat]:
		app.xpr.vars["CATEGORIES"].pop(cat)
	#app.xpr.vars["CATEGORIES"].pop(counter.contents.winfo_children().index(frame))
	frame.pack_forget()
	frame.destroy()
	update_scrollbars(counter)
	
## Retrieve molar radioactivity from a radiosheet
def retrieve_molrad_from_sheet(sheet):
	sheet_df = pd.read_excel(sheet, header=None)
	if len(sheet_df) >= 49 and len(sheet_df.columns) >= 6 and sheet_df.iloc[48, 5] == "DPM/pmol":
		return sheet_df.iloc[48, 4] * 1e12
	elif len(sheet_df) >= 34 and len(sheet_df.columns) >= 5 and sheet_df.iloc[33, 4] == "DPM/pmol":
		return sheet_df.iloc[33, 3] * 1e12
	elif len(sheet_df) >= 31 and len(sheet_df.columns) >= 4 and	sheet_df.iloc[30, 1] == "1 pmol equals":
		return  sheet_df.iloc[30, 4] * 1e12
	elif len(sheet_df) >= 30 and len(sheet_df.columns) >= 4 and	sheet_df.iloc[29, 1] == "1 pmol equals":
		return  sheet_df.iloc[29, 4] * 1e12
	showerror(title="Error", message="Unable to read DPM/pmol from the "
									 "radiosheet. Make sure the sheet i"
									 "s properly formatted or enter the"
									 " radio compound manually.")

## Display the pre-defined molar radioactivity.
def display_predef_molar_radioactivity(app, compound_combo, batch_combo, entry):
	compound = compound_combo.get()
	batch = batch_combo.get()
	sheet = [tup for tup in app.radio_compounds[compound] if tup[0] == batch][0][1]
	sheet = f"{app.config['radio_sheet_dir']}/{sheet}"
	molrad = retrieve_molrad_from_sheet(sheet)
	#entry.config(state="enabled")
	entry.delete(0, tk.END)
	entry.insert(0, f"{molrad:.3g}")
	#entry.config(state="disabled")

'''	
## Increment treatment level
def increment_treatment_level(label):
	current_level = int(label.cget("text"))
	label.config(text=f"{current_level+1}")

## Decrement treatment level
def decrement_treatment_level(label):
	current_level = int(label.cget("text"))
	label.config(text=f"{max(current_level-1, 0)}")
'''