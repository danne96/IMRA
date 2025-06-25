import tkinter as tk
from tkinter import ttk

from ..session import Session

class NewExperimentStart(ttk.Frame):
	
	def __init__(self, container, app: Session, is_temp = False, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		
		# Project ID
		## Label
		name_label = ttk.Label(self, text=f"Enter a unique name for the new {["experiment", "template"][is_temp]}.\n"
						 				   "NOTE: The name must start with a letter [a-zA-Z] or a digit [0-9].")
		name_label.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=10, pady=(10, 5))
		## Entry
		name_entry = ttk.Entry(self, width=60)
		name_entry.focus()
		name_entry.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=10, pady=(0, 10))

		if not is_temp:
			# Project template
			## Label
			temp_label = ttk.Label(self, text="(Optional) Select a template for your experiment.")
			temp_label.grid(column=0, row=2, sticky=tk.W, padx=10, pady=(10, 5))
			## Combobox
			temp_combo = ttk.Combobox(self, values=["--None--"] + app.tmp_list_names)
			temp_combo.current(0)
			temp_combo.grid(column=0, row=3, sticky=tk.W, padx=10, pady=(0, 10))
			
			this_row = 4
		else:
			this_row = 2
	
		# Decription
		desc = ttk.Frame(self)
		desc.grid(column=0, row=this_row, columnspan=2, sticky=tk.W+tk.E, padx=10, pady=10)
		## Label
		desc_label = ttk.Label(desc, text=f"(Optional) Provide a brief description of the {["experiment", "template"][is_temp]}:")
		desc_label.grid(column=0, row=1, columnspan=2, sticky=tk.W, pady=(0, 5))
		## Text
		#desc_text = ScrolledText(self, width=20, height=10, bg="white", fg="black", font="TkDefautltFont 10")
		#desc_text.grid(column=0, row=5, sticky=tk.W+tk.E, padx=10, pady=(5,10), columnspan=2)
		desc_text = tk.Text(desc, width=60, height=10, bg="white", fg="black", font="TkDefautltFont 10", wrap="word")
		desc_text.grid(column=0, row=1, sticky=tk.W+tk.E)#, padx=(5, 0), pady=5)
		desc_text_yscroll = ttk.Scrollbar(desc, orient="vertical", command=desc_text.yview)
		desc_text_yscroll.grid(column=1, row=1, sticky="ns")#, padx=(0, 5), pady=5)
		desc_text.configure(yscrollcommand=desc_text_yscroll.set)
	
		# Navigation
		cancel_btn = ttk.Button(self, text="Cancel", command=lambda: container.destroy()) ## the container of the container is the window
		cancel_btn.grid(column=0, row=this_row+1, padx=10, pady=(5, 10), sticky=tk.W)

		commands = [lambda: self.master.create_new_experiment(app, name_entry.get(), desc_text.get("1.0","end-1c"), temp_combo.get()),
			  		lambda: self.master.create_new_template(app, name_entry.get(), desc_text.get("1.0","end-1c"))]
		enter_btn = ttk.Button(self, text="Enter",
							   command=commands[is_temp])
		enter_btn.grid(column=1, row=this_row+1, padx=10, pady=(5, 10), sticky=tk.E)        
