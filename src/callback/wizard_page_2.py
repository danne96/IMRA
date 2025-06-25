from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showerror

import os
import re
import numpy as np
from striprtf.striprtf import rtf_to_text


from ..widgets.ExperimentalRunManagerRow import ExperimentalRunManagerRow
from .update_scrollbars import update_scrollbars

def select_t_file(container, app, check_label, disp_label=None, width=50):
	if app.xpr.path_to_t and os.path.exists(app.xpr.path_to_t):
		initialdir = os.path.dirname(app.xpr.path_to_t)
	else:
		initialdir="."
	fname = fd.askopenfilename(parent=container,
							   title="Select a timing file",
							   initialdir=initialdir,
							   filetypes=[("All file formats", "*.*"),
								   		  ("TXT, Text file format", "*.txt"),
										  ("CSV, Comma-separated file format", "*.csv"),
										  #("XLSX, Microsoft Excel spreadsheet file format", "*.xlsx"),
										  #("XLS, Microsoft Excel 97-2003 spreadsheet file format", "*.xls")
										  ])
	if fname:
		app.xpr.path_to_t = fname
		check_t_file(app, check_label)
	
		disp_text = os.path.abspath(fname)
		if len(disp_text) > width:
			disp_text = f"{disp_text[:9]}...{disp_text[-39:]}"
		disp_label.config(text=disp_text)

## Update the timing file info
def check_t_file(app, label):
	if not app.xpr.path_to_t:
		label.config(text="No file", font="TkDefaultFont 10 bold", foreground="blue")
	else:
		try:
			read_t(app, app.xpr.path_to_t)
			label.config(text=f"{len(app.xpr.raw_data['TIME'])} samples found", font="TkDefaultFont 10 bold", foreground="green")
		except Exception:
			label.config(text="ERROR", font="TkDefaultFont 10 bold", foreground="red")

## Read a timing file
def read_t(app, path_to):
	with open(path_to, "r") as tfile:
		lines = [line[:-1] for line in tfile]
	## Check for possible column delimiters: commas, white space, colons, full stops
	lines = [re.split(r"[\s,:\.]+", line) for line in lines]
	## Check for an optional non-numeric header and remove it
	if not all(map(lambda x: x.isdigit(), lines[0])):
		lines = lines[1:]
	lines = [list(map(int, row)) for row in lines]
	## Two columns are interpreted as minutes and seconds; convert to seconds only
	if len(lines[0]) == 2:
		lines = [lines[ii][0] * 60 + lines[ii][1] for ii in range(len(lines))]
	else:
		lines = [lines[ii][0] for ii in range(len(lines))]
	app.xpr.raw_data["TIME"] = lines
				
	
## Browse DPM files
def select_DPM_file(container, app, check_label, blanks, disp_label, width=50):
	fname = fd.askopenfilename(parent=container,
							   title="Select a measurement report file",
							   initialdir=".", # TODO: make adjustable
							   filetypes=[("All file formats", "*.*"),
								   		  ("TXT, Text file format", "*.txt"),
								   		  ("RTF, Rich text file format", "*.rtf"),
										  ("CSV, Comma-separated file format", "*.csv")
										  ])
	if fname:
		app.xpr.path_to_DPM = fname
		app.xpr.blanks = blanks
		check_DPM_file(app, check_label)
		disp_text = os.path.abspath(fname)
		if len(disp_text) > width:
			disp_text = f"{disp_text[:9]}...{disp_text[-39:]}"
		disp_label.config(text=disp_text)

## Update the DPM file info
def check_DPM_file(app, label):
	if not app.xpr.path_to_DPM:
		label.config(text="No file", font="TkDefaultFont 10 bold", foreground="blue")
	else:
		try:
			read_DPM(app, app.xpr.path_to_DPM, app.xpr.blanks)
			label.config(text=f"{len(app.xpr.raw_data['DPM'])} samples found", font="TkDefaultFont 10 bold", foreground="green")
		except Exception:
			label.config(text="ERROR", font="TkDefaultFont 10 bold", foreground="red")

## Read a DPM file in RTF or TXT format
def read_DPM(app, path_to, blanks):
	DPM = []
	write = 0
	isRTF = os.path.splitext(path_to)[1] == ".rtf"
	with open(path_to, "r") as FILE:
		for line in FILE:
			if isRTF:
				line = rtf_to_text(line)
			line = line.strip()
			if re.search("S#(?=.*DPM1)", line):
				DPM.append([])
				DPM_pos = re.split(r"\s{2,}|,", line).index("DPM1")
				write = 1
			elif write and re.search("[0-9]", line) and not re.search("Missing vial [0-9]+", line) and not re.search("Cycle [0-9]+ [rR]esults", line):
				line = re.split(r"\s{2,}|,", line)
				DPM[-1].append(float(line[DPM_pos]))
		
	#### SUBTRACT BLANKS???
	if blanks[1]:
		DPM = [dset[blanks[0]:-blanks[1]] for dset in DPM]
	else:
		DPM = [dset[blanks[0]:] for dset in DPM]
	#### TODO: Discuss with PK how to deal with outliers
	app.xpr.raw_data["DPM"] = list(np.median(DPM, 0))
	
# ADD AND MODIFY EXPERIMENTAL RUNS
## Add runs to a scrollable frame and update the project data
def add_rows_to_run_manager(container, app, rows):
	for row in rows:
		row.pack()
		app.xpr.runs.append([int(row.samps.get()), float(row.svol.get()), float(row.radio_c.get()), row.cond.get()])
	update_scrollbars(container)
def add_rows_to_run_manager_button(container, app, samp_count_entry: ttk.Entry, samp_vol_entry: ttk.Entry,
								   radio_conc_entry: ttk.Entry, runs_to_add_entry: ttk.Entry):
	try:
		samp_count = int(samp_count_entry.get())
		if samp_count <= 0:
			showerror(title="Error", parent=container.master.master,
			          message="The sample count must be greater than zero.")
			return
	except ValueError:
		showerror(title="Error", parent=container.master.master,
				  message="The sample count is not a valid integer.")
		return
	
	try:
		samp_vol = float(samp_vol_entry.get())
		if samp_vol <= 0:
			showerror(title="Error", parent=container.master.master,
			          message="The sample volume must be greater than zero.")	
			return		
	except ValueError:
		showerror(title="Error", parent=container.master.master,
				  message="The sample volume is not a valid floating-point number.")
		return
	
	try:
		radio_conc = float(radio_conc_entry.get())
		if radio_conc <= 0:
			showerror(title="Error", parent=container.master.master,
			          message="The tracer concentration must be greater than zero.")
			return
	except ValueError:
		showerror(title="Error", parent=container.master.master,
				  message="The tracer concentration is not a valid floating-point number.")
		return
	
	try:
		runs_to_add = int(runs_to_add_entry.get())
		if runs_to_add <= 0:
			showerror(title="Error", parent=container.master.master,
			          message="The number of runs to be added must be greater than zero.")
			return
	except ValueError:
		showerror(title="Error", parent=container.master.master,
				  message="The number of runs to be added is not a valid integer.")
		return
	
	rows = [ExperimentalRunManagerRow(container, app, samp_count, samp_vol, radio_conc) for _ in range(runs_to_add)]
	add_rows_to_run_manager(container, app, rows)
	

## Assign a new condition to an experimental run	
def update_row_in_run_manager(container, app, row):
	run_nr = container.contents.winfo_children().index(row)
	app.xpr.runs[run_nr][3] = row.cond.get()
	
## Remove experimental run from the run manager
def remove_row_from_run_manager(container, app, row):
	run_nr = container.contents.winfo_children().index(row)
	app.xpr.runs.pop(run_nr)
	row.pack_forget()
	row.destroy()

	for i, child in enumerate(container.contents.winfo_children()):
		child.run_num.config(text=f"{i+1:02d}")
	update_scrollbars(container)