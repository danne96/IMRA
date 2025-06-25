import math

from .update_scrollbars import update_scrollbars

## Add runs to a scrollable frame and update the project data
def add_rows_to_run_manager(container, app, rows):
	for row in rows:
		row.pack()
		app.xpr.runs.append([int(row.samps.get()), float(row.svol.get()), float(row.radio_c.get()), row.cond.get()])
	update_scrollbars(container)

## Remove experimental run from the run manager
def remove_row_from_run_manager(container, app, row):
	run_nr = container.contents.winfo_children().index(row)
	app.xpr.runs.pop(run_nr)
	row.pack_forget()
	row.destroy()

	for i, child in enumerate(container.contents.winfo_children()):
		child.run_num.config(text=f"{i+1:02d}")
	update_scrollbars(container)	

## Assign a new condition to an experimental run	
def update_row_in_run_manager(container, app, row):
	run_nr = container.contents.winfo_children().index(row)
	app.xpr.runs[run_nr][3] = row.cond.get()

## Validate and update sample count in an experimental run
def update_sample_count(app, row):
	try:
		app.xpr.runs[row.num-1][0] = int(row.samps_var.get())
	except ValueError:
		try:
			row.samps_var.set(math.floor(float(row.samps_var.get())))
			app.xpr.runs[row.num-1][0] = int(row.samps_var.get())
		except ValueError:
			row.samps_var.set(app.xpr.runs[row.num-1][0])
			
## Validate and update sample volume in an experimental run
def update_sample_volume(app, row):
	try:
		app.xpr.runs[row.num-1][1] = float(row.svol_var.get())
	except ValueError:
		row.svol_var.set(app.xpr.runs[row.num-1][1])
			
## Validate and update tracer concentration in an experimental run
def update_tracer_concentration(app, row):
	try:
		app.xpr.runs[row.num-1][2] = float(row.radio_c_var.get())
	except ValueError:
		row.radio_c_var.set(app.xpr.runs[row.num-1][2])

