import tkinter as tk
from tkinter import ttk

from ..callback.experiment_browser import *

class ExperimentBrowser(ttk.Frame):
	def __init__(self, container, app, is_temp=False, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		self.app = app
		self.write_xlsx = tk.IntVar(value=0) # when changing experiment name or decription
		self.delete_xlsx = tk.IntVar(value=0) # ditto

		## Experiment list frame
		eli = ttk.Frame(self)
		eli.grid(column=0, row=0, padx=5, pady=5, rowspan=2, sticky="nw")
		#### List label
		eli_lab = ttk.Label(eli, text=f"Select a{["n experiment", " template"][is_temp]} from the list below:")
		eli_lab.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
		#### List container
		eli_lbx = tk.Listbox(eli, width=40, height=12, exportselection=False)
		eli_lbx.grid(column=0, row=1, padx=(5, 0), sticky="ns", pady=(5, 0))
		eli_lbx_xscroll = ttk.Scrollbar(eli, orient="horizontal", command=eli_lbx.xview)
		eli_lbx_xscroll.grid(column=0, row=2, padx=5, sticky="ew", pady=(0, 5))
		eli_lbx_yscroll = ttk.Scrollbar(eli, orient="vertical", command=eli_lbx.yview)
		eli_lbx_yscroll.grid(column=1, row=1, padx=(0, 5), sticky="ns", pady=5)
		eli_lbx.configure(xscrollcommand=eli_lbx_xscroll.set, yscrollcommand=eli_lbx_yscroll.set)
		for ii, xpr in enumerate([app.xpr_list_names, app.tmp_list_names][is_temp]):
			eli_lbx.insert(ii, xpr)
		self.eli_lbx = eli_lbx ## the listbox will be accessed by other methods

		## Description frame
		des = ttk.Frame(self)
		des.grid(column=1, row=0, padx=5, pady=5, sticky="nw")
		#### Description label
		des_lab = ttk.Label(des, text=f"{["Experiment", "Template"][is_temp]} description:")
		des_lab.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
		#### Description scrolled text
		des_txt = tk.Text(des, width=40, height=5, bg="lightgray", fg="black", font="TkDefautltFont 10", wrap="word")
		des_txt.config(state="disabled")
		des_txt.grid(column=0, row=1, padx=(5, 0), pady=5)
		des_txt_yscroll = ttk.Scrollbar(des, orient="vertical", command=des_txt.yview)
		des_txt_yscroll.grid(column=1, row=1, padx=(0, 5), pady=5, sticky="ns")
		des_txt.configure(yscrollcommand=des_txt_yscroll.set)

		## Display description of the currently selected experiment
		eli_lbx.bind("<<ListboxSelect>>", lambda e: display_description(e, self.app, des_txt, is_temp)) 

		## Button frame
		btf = ttk.Frame(self)
		btf.grid(column=1, row=1, padx=5, pady=5, sticky="nw")
		#### Button desc
		btf_lab = ttk.Label(btf, text="Configure the selected experiment")
		btf_lab.grid(column=0, row=0, padx=5, pady=5, sticky="nw", columnspan=2)
		#### NW Button: Edit name
		btn_name = ttk.Button(btf, text="Edit name", width=17, command=lambda: self.edit_name_widget(is_temp))
		btn_name.grid(column=0, row=1, padx=5, pady=5)
		#### NE Button: Edit description
		btn_desc = ttk.Button(btf, text="Edit description", width=17, command=lambda: self.edit_description_widget(is_temp))
		btn_desc.grid(column=1, row=1, padx=5, pady=5)
		#### SW Button: Modify experiment
		btn_mod = ttk.Button(btf, text=f"Modify {["experiment", "template"][is_temp]}", width=17, command=lambda: modify(self.app, self.eli_lbx, is_temp))
		btn_mod.grid(column=0, row=2, padx=5, pady=5)
		#### SE Button: Delete experiment
		btn_del = ttk.Button(btf, text=f"Delete {["experiment", "template"][is_temp]}", width=17, command=lambda: delete(self.app, self.eli_lbx, is_temp))
		btn_del.grid(column=1, row=2, padx=5, pady=5)
		#### Far south Button: Back to menu
		btn_back = ttk.Button(btf, text="Back to main menu", width=17, command=self.master.destroy)
		btn_back.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="we")

	## A destroy method that also returns focus to the listbox
	def destroy_child_win(self, win):
		win.destroy()
		self.eli_lbx.focus()

	## Display a window allowing the user to pick a new experiment name
	def edit_name_widget(self, is_temp: bool):
		win = tk.Toplevel(self)
		win.resizable(False, False)
		win.title(f"Edit {["experiment", "template"][is_temp]} name")

		frm = ttk.Frame(win)
		frm.pack(padx=5, pady=5)

		## Label
		lab = ttk.Label(frm, text="Please, insert a new name:")
		lab.grid(column=0, row=0, padx=5, pady=(5, 0), sticky="w")

		## Entry
		ent = ttk.Entry(frm, width=32)
		ent.grid(column=1, row=0, padx=(0, 5), pady=5, sticky="e")

		## Bottom label
		lab2 = ttk.Label(frm, text="The name has to start with a letter or a digit.")
		lab2.grid(column=0, row=1, columnspan=2, padx=5, pady=(0, 5), sticky="w")
		
		if is_temp:
			this_row = 2
		else:
			## Write XLSX check
			write_xlsx_check = ttk.Checkbutton(frm, text="Write a new XLSX?\n"
									                 	 "(Only applies to experiments with an existing XLSX output path)",
										   	   variable=self.write_xlsx)
			write_xlsx_check.grid(column=0, row=2, columnspan=2, padx=5, pady=(10, 5), sticky="w")

			## Delete XLSX check
			delete_xlsx_check = ttk.Checkbutton(frm, text="Delete the existing XLSX?\n"
									  				  	  "(Only applies if the ouput path and file name have not been changed)",
												variable=self.delete_xlsx)
			delete_xlsx_check.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="w")
			this_row = 4

		## Cancel button
		cancel_btn = ttk.Button(frm, text="Cancel", command=lambda: self.destroy_child_win(win))
		cancel_btn.grid(column=0, row=this_row, padx=5, pady=5, sticky="w")

		## Confirm button
		confirm_btn = ttk.Button(frm, text="Confirm", command=lambda: edit_name(self.app, self.eli_lbx, win, ent.get(), self.write_xlsx.get(),
																		  		self.delete_xlsx.get(), is_temp))
		confirm_btn.grid(column=1, row=this_row, padx=5, pady=5, sticky="e")

	## Display a window allowing the user to edit experiment description
	def edit_description_widget(self, is_temp: bool):
		win = tk.Toplevel(self)
		win.resizable(False, False)
		win.title(f"Edit {["experiment", "template"][is_temp]} description")

		frm = ttk.Frame(win)
		frm.pack(padx=5, pady=5)

		## Label
		lab = ttk.Label(frm, text="Please, edit the description in the text field below:")
		lab.grid(column=0, row=0, columnspan=3, padx=5, pady=5, sticky="w")

		## Text
		des = tk.Text(frm, width=80, height=10, bg="white", fg="black", font="TkDefautltFont 10", wrap="word")
		des.grid(column=0, row=1, columnspan=2, padx=(5, 0), pady=(0, 5), sticky="w")
		des_yscroll = ttk.Scrollbar(frm, orient="vertical", command=des.yview)
		des_yscroll.grid(column=2, row=1, padx=(0, 5), pady=(0, 5), sticky="ns")
		des.configure(yscrollcommand=des_yscroll.set)
		#### Display the current description
		xpr = load_from_listbox(self.app, self.eli_lbx, is_temp)
		des.insert(tk.END, xpr.desc)

		## Write XLSX check
		if not is_temp:
			write_xlsx_check = ttk.Checkbutton(frm, text="Write a new XLSX? (Only applies to experiments with an existing XLSX output path)",
											   variable=self.write_xlsx)
			write_xlsx_check.grid(column=0, row=2, columnspan=3, padx=5, pady=(10, 5), sticky="w")

		## Cancel button
		cancel_btn = ttk.Button(frm, text="Cancel", command=lambda: self.destroy_child_win(win))
		cancel_btn.grid(column=0, row=3-is_temp, padx=5, pady=5, sticky="w")

		confirm_btn = ttk.Button(frm, text="Confirm", command=lambda: edit_description(self.app, self.eli_lbx, win, des.get("1.0", tk.END)[:-1],
																					   self.write_xlsx.get(), is_temp))
		confirm_btn.grid(column=1, row=3-is_temp, padx=5, pady=5, sticky="e")	

