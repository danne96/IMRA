import tkinter as tk
from tkinter.messagebox import askyesno

import json
import os

from .xpr2xlsx import xpr2xlsx
from ..experiment.Experiment import Experiment, Template
from ..session import Session
from ..widgets.NewExperimentWizard import ModifyExperimentWizard

def load_from_listbox(app, lbox, is_temp: bool):
	'''
	Create an experiment or template instance based on the name the user has picked from the listbox in the browser.
	'''
	name = lbox.get(lbox.curselection()[0])
	if is_temp:
		with open(f"{app.config["template_dir"]}/{name}.json", "r") as afile:
			return Template(**json.load(afile))
	else:
		with open(f"{app.config["experiment_dir"]}/{name}.json", "r") as afile:
			return Experiment(**json.load(afile))		

def display_description(event, app, out_widget: tk.Text, is_temp: bool):
	'''
	Show the description of the user-selected experiemnt or template name in the right-hand part of the browser.
	'''
	xpr = load_from_listbox(app, event.widget, is_temp)
	out_widget.config(state="normal")
	out_widget.delete(1.0, tk.END)
	if xpr.desc:
		out_widget.insert(tk.END, xpr.desc)
	else:
		out_widget.insert(tk.END, "-- no description provided --")
	out_widget.config(state="disabled")

def edit_name(app: Session, lbox: tk.Listbox, container: tk.Toplevel, new_name: str,
						 write_xlsx: bool, delete_xlsx: bool, is_temp: bool):
	lbox_ndx = lbox.curselection()[0]
	#### Change the name and save a new file
	xpr = load_from_listbox(app, lbox, is_temp)
	old_name, xpr.name = xpr.name, new_name
	xpr.save(app)
	if write_xlsx and xpr.xlsx_out_dir and os.path.exists(f"{xpr.xlsx_out_dir}/"):
		xpr2xlsx(xpr)
	#### Remove the old files		
	os.remove(f"{app.config[["experiment_dir", "template_dir"][is_temp]]}/{old_name}.json")
	if delete_xlsx and os.path.exists(f"{xpr.xlsx_out_dir}/{old_name}.xlsx"):
		os.remove(f"{xpr.xlsx_out_dir}/{old_name}.xlsx")
	#### Update the listbox entry
	lbox.delete(lbox_ndx)
	lbox.insert(lbox_ndx, new_name)
	#### Select the updated entry
	lbox.selection_set(lbox_ndx)
	lbox.activate(lbox_ndx)
	lbox.focus()
	lbox.event_generate("<<ListboxSelect>>")
	if is_temp:
		app.update_templates()
	else:
		app.update_experiments()
	#### Destroy the edit name window
	container.destroy()

def edit_description(app: Session, lbox: tk.Listbox, container: tk.Toplevel, new_desc: str,
					 write_xlsx: bool, is_temp: bool):
	xpr = load_from_listbox(app, lbox, is_temp)
	xpr.desc = new_desc
	xpr.save(app)
	if write_xlsx and xpr.xlsx_out_dir and os.path.exists(f"{xpr.xlsx_out_dir}/"):
		xpr2xlsx(xpr)
	lbox.event_generate("<<ListboxSelect>>")
	lbox.focus()
	container.destroy()

def modify(app: Session, lbox: tk.Listbox, is_temp: bool):
	xpr = load_from_listbox(app, lbox, is_temp)
	app.xpr = xpr
	window = ModifyExperimentWizard(app, is_template=is_temp)
	window.title(f"Modify {["Experiment", "Template"][is_temp]}: {xpr.name}")
	#page_container = ModifyExperimentWizard(window, app)
	#page_container.pack(padx=5, pady=5)

def delete(app: Session, lbox: tk.Listbox, is_temp: bool):
	confirm = askyesno(title=f"Delete {["experiment", "template"][is_temp]}",
					   message=f"Removing a{["n experiment", " template"][is_temp]} cannot be undone. Please, confirm your choice.")	
	if confirm:
		xpr = load_from_listbox(app, lbox, is_temp)
		if is_temp:
			os.remove(f"{app.config["template_dir"]}/{xpr.name}.json")
			app.update_templates()
		else:
			os.remove(f"{app.config["experiment_dir"]}/{xpr.name}.json")
			app.update_experiments()
		lbox_ndx = lbox.curselection()[0]
		lbox.delete(lbox_ndx)
		if lbox_ndx > 0:
			lbox.selection_set(lbox_ndx-1)
		else:
			lbox.selection_set(0)
		if xpr.xlsx_out_dir and os.path.exists(f"{xpr.xlsx_out_dir}/{xpr.name}.xlsx"):
			delete_xlsx = askyesno(title="Delete experiment",
						 		   message="A XLSX file related to the deleted experiment was found. Do you want to remove it too?")
			if delete_xlsx:
				os.remove(f"{xpr.xlsx_out_dir}/{xpr.name}.xlsx")
		lbox.event_generate("<<ListboxSelect>>")
		lbox.focus()
