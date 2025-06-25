import os
import xlsxwriter
import platform
import numpy as np

from ..models.models import MODELS
from ..experiment.Experiment import Experiment

def xpr2xlsx(xpr: Experiment):
	'''
	Save the experiment info as an Excel sheet.
	'''
	if os.path.exists(f"{xpr.xlsx_out_dir}/{xpr.name}.xlsx"):
		os.remove(f"{xpr.xlsx_out_dir}/{xpr.name}.xlsx")
	wb = xlsxwriter.Workbook(f"{xpr.xlsx_out_dir}/{xpr.name}.xlsx", {'nan_inf_to_errors': True})
	## Add formats
	bold_format = wb.add_format({"bold": True})
	title_format = wb.add_format({"bold": True, "bg_color": "#ff5429", "font_color": "#ffffff"})
	subtitle_format = wb.add_format({"bold": True, "bg_color": "#ffffa6"})
	merge_format = wb.add_format({"text_wrap": True})
	merge_format.set_align("vjustify")
	row_head_format = wb.add_format({"italic": True, "text_wrap": 1})
	row_head_format.set_align("vjustify")
	row_head_format.set_align("bottom")
	col_head_format = wb.add_format({"bold": True, "text_wrap": 1})
	col_head_format.set_align("vjustify")
	col_head_format.set_align("bottom")
	matrix_elem_format = wb.add_format()
	matrix_elem_format.set_align("center")
	matrix_elem_format.set_align("vcenter")
	samp_found_format = wb.add_format({"bold": True, "align": "center"})
	if platform.system() == "Linux":
		for fmt in wb.formats:
			fmt.set_font_name("Liberation Sans")
			fmt.set_font_size(10)
	## Summary sheets
	summ = wb.add_worksheet("Summary")
	summ.set_column("A:A", width=15)
	summ.set_column("B:P", width=11)
	#### Title
	summ.write(0, 0, "Project Name:")
	summ.write(0, 2, xpr.name)
	summ.set_row(0, cell_format=title_format)
	#### Decription
	summ.write(1, 0, "Description:")
	summ.set_row(1, cell_format=subtitle_format)
	summ.merge_range("A3:P3", xpr.desc, merge_format)
	#### Conditions
	summ.write(3, 0, "Experimental conditions:")
	summ.set_row(3, cell_format=subtitle_format)
	summ.write(4, 0, "Cell line", bold_format)
	summ.write(5, 0, "Suspension density * mL", row_head_format)
	summ.set_row(5, height=25)
	summ.write(6, 0, "Average cell volume / m^3", row_head_format)
	summ.set_row(6, height=25)
	for i, susp in enumerate(xpr.vars["SUSPENSIONS"].keys()):
		summ.write(4, i+1, susp)
		summ.write(5, i+1, xpr.vars["SUSPENSIONS"][susp], matrix_elem_format)
		summ.write(6, i+1, xpr.vars["CELL_LINE_BCKG"][susp.split(":")[1]], matrix_elem_format)
	summ.write(8, 0, "Tracer", bold_format)
	summ.write(9, 0, "Molar activity / (DPM/mol)", row_head_format)
	summ.set_row(9, height=25)
	for i, trac in enumerate(xpr.vars["RADIOCHEMICALS"].keys()):
		summ.write(8, i+1, trac)
		summ.write(9, i+1, xpr.vars["RADIOCHEMICALS"][trac], matrix_elem_format)
	summ.write(11, 0, "Category", row_head_format)
	this_row = 11
	for i, cat in enumerate(xpr.vars["CATEGORIES"].keys()):
		summ.write(11, i+1, cat, bold_format)
		for j, val in enumerate(xpr.vars["CATEGORIES"][cat]):
			summ.write(j+12, i+1, val)
			this_row = max([j+12, this_row])
	this_row += 2
	summ.write(this_row, 0, "The following experimental CONDITIONS (denoted A, B, ...) were generated from the variables listed above:")
	summ.write(this_row+1, 0, "Condition", bold_format)
	summ.write(this_row+2, 0, "Tracer", row_head_format)
	summ.write(this_row+3, 0, "Suspension", row_head_format)
	summ.write(this_row+4, 0, "Background", row_head_format)
	for i, cat in enumerate(xpr.vars["CATEGORIES"].keys()):
		summ.write(this_row+5+i, 0, cat, row_head_format)
	for j, cond in enumerate(xpr.conds.keys()):
		summ.write(this_row+1, j+1, cond, bold_format)
		summ.write(this_row+2, j+1, xpr.conds[cond][0])
		summ.write(this_row+3, j+1, xpr.conds[cond][1].split(":")[0])
		summ.write(this_row+4, j+1, xpr.conds[cond][1].split(":")[1])
		for i, _ in enumerate(xpr.vars["CATEGORIES"].keys()):
			summ.write(this_row+5+i, j+1, xpr.conds[cond][i+2])
	this_row += 5 + len(xpr.vars["CATEGORIES"].keys())
	#### Runs
	summ.write(this_row, 0, "Raw data and experimental runs:")
	summ.set_row(this_row, cell_format=subtitle_format)
	summ.write(this_row+1, 0, "Timing data were read from:")
	summ.write(this_row+1, 2, os.path.abspath(xpr.path_to_t))
	summ.write(this_row+2, 0, "There were")
	summ.write(this_row+2, 1, len(xpr.raw_data["TIME"]), samp_found_format)
	summ.write(this_row+2, 2, "samples")
	summ.write(this_row+3, 0, "DPM data were read from:")
	summ.write(this_row+3, 2, os.path.abspath(xpr.path_to_DPM))
	summ.write(this_row+4, 0, "There were")
	summ.write(this_row+4, 1, len(xpr.raw_data["TIME"]), samp_found_format)
	summ.write(this_row+4, 2, "samples")
	summ.write(this_row+6, 0, "These samples are distributed among following RUNS:")
	summ.write(this_row+7, 0, "Run #", col_head_format)
	summ.write(this_row+7, 1, "Sample Count", col_head_format)
	summ.write(this_row+7, 2, "Sample Vol. / m^3", col_head_format)
	summ.write(this_row+7, 3, "Tracer Con. / (mol / m^3)", col_head_format)
	summ.write(this_row+7, 4, "Condition", col_head_format)
	this_row += 8
	for i in range(len(xpr.runs)):
		this_row_cont = [i+1] + xpr.runs[i]
		for j in range(len(this_row_cont)):
			summ.write(this_row+i, j, this_row_cont[j])

	this_row += i + 2
	summ.write(this_row, 0, "Plot data and modelling parameters")
	summ.set_row(this_row, cell_format=subtitle_format)
	if xpr.models["EXP"]:
		summ.write(this_row+1, 0, "Exponential model (EXP)")
		summ.write(this_row+2, 0, "Y(t) = c0 * L * [1 - e^(-t * S)] + K")
		summ.write(this_row+3, 0, "Run #", col_head_format)
		summ.write(this_row+3, 1, "L", col_head_format)
		summ.write(this_row+3, 2, "S * s", col_head_format)
		summ.write(this_row+3, 3, "K / (mol)", col_head_format)
		for i in range(len(xpr.runs)):
			summ.write(this_row+4+i, 0, i+1)
			summ.write(this_row+4+i, 1, xpr.results["EXP"]["L"][i])
			summ.write(this_row+4+i, 2, xpr.results["EXP"]["S"][i])
			summ.write(this_row+4+i, 3, xpr.results["EXP"]["K"][i])
		this_row += i+5
	if xpr.models["EXP_1K"]:
		summ.write(this_row+1, 0, "Exponential model with common K (EXP_1K)")
		summ.write(this_row+2, 0, "Y(t) = c0 * L * [1 - e^(-t * S)] + K; K -> R^1")
		summ.write(this_row+3, 0, "K = ")
		summ.write(this_row+3, 1, xpr.results["EXP_1K"]["K"])
		summ.write(this_row+4, 0, "Run #", col_head_format)
		summ.write(this_row+4, 1, "L", col_head_format)
		summ.write(this_row+4, 2, "S * s", col_head_format)
		for i in range(len(xpr.runs)):
			summ.write(this_row+5+i, 0, i+1)
			summ.write(this_row+5+i, 1, xpr.results["EXP_1K"]["L"][i])
			summ.write(this_row+5+i, 2, xpr.results["EXP_1K"]["S"][i])
		this_row += i+6
	if xpr.models["EXP_0K"]:
		summ.write(this_row+1, 0, "Exponential model with the intercept at (0, 0); i.e. K = 0 (EXP_0K)")
		summ.write(this_row+2, 0, "Y(t) = c0 * L * [1 - e^(-t * S)]")
		summ.write(this_row+3, 0, "Run #", col_head_format)
		summ.write(this_row+3, 1, "L", col_head_format)
		summ.write(this_row+3, 2, "S * s", col_head_format)
		for i in range(len(xpr.runs)):
			summ.write(this_row+4+i, 0, i+1)
			summ.write(this_row+4+i, 1, xpr.results["EXP_0K"]["L"][i])
			summ.write(this_row+4+i, 2, xpr.results["EXP_0K"]["S"][i])
	# Plot data sheets
	if xpr.write_plot_data:
		plot = wb.add_worksheet("Plot Data")
		plot.set_row(0, cell_format=title_format)
		plot.set_row(1, cell_format=subtitle_format)
		plot.write(0, 0, "Measured Data")
		if sum(xpr.models.values()):
			plot.write(0, 7, "Modelled Data")
			T = np.arange(xpr.plot_from, xpr.plot_to + xpr.plot_timestep / 1e3, xpr.plot_timestep / 1e3)
			plot.write(1, 7, "Time / s")
			plot.write_column(2, 7, T)
		plot.write(1, 0, "Time / s")
		plot.write_column(2, 0, xpr.raw_data["TIME"])
		plot.write(1, 1, "DPM")
		plot.write_column(2, 1, xpr.raw_data["DPM"])
		plot.write(1, 2, "DPM per 10^6 cells")
		plot.write_column(2, 2, np.array(xpr.processed_data["DPMC"]).flatten())
		plot.write(1, 3, "Conc. / (nmol / L)")
		plot.write_column(2, 3, np.array(xpr.processed_data["Y"]).flatten())
		plot.write(1, 4, "Run #")
		plot.write(1, 5, "Condition")
		i = 0
		for j, run in enumerate(xpr.runs):
			plot.write_column(2+i, 4, [j+1] * run[0])
			plot.write_column(2+i, 5, [run[3]] * run[0])
			i += run[0]

		if sum(xpr.models.values()):
			for k, mod in enumerate(xpr.models.keys()):
				plot.write(0, 9 + k * (len(xpr.runs) + 1), mod)
				mod_plot_data = MODELS[mod][3](xpr, T).transpose()
				for m in range(len(xpr.runs)):
					plot.write(1, 9 + k * (len(xpr.runs) + 1) + m, f"Run #{m+1}")
					plot.write_column(2, 9 + k * (len(xpr.runs) + 1) + m, mod_plot_data[:, m])
		
	wb.close()