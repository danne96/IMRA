import tkinter as tk
from tkinter import ttk

from .session import Session
from .widgets.Configure import Configure
from .widgets.ExperimentBrowser import ExperimentBrowser
from .widgets.NewExperimentWizard import NewExperimentWizard

class GUI:

	def __init__(self):
		## Create an instance of the Session object to hold information about the current experiment
		## and configuration
		self.app = Session()

		## Create the main window
		self.root = tk.Tk()
		self.root.title("IMRA")
		self.root.resizable(False, False)

		message1 = tk.Label(self.root, text="Welcome to...")
		message1.pack(pady=(20, 0))

		namefr = tk.Frame(self.root)#, background="white")
		namefr.pack(padx=40, pady=25)
		letter_I = tk.Label(namefr, text="I", font=("Courier", 14, "bold"), foreground="blue")
		letter_I.grid(column=0, row=0, sticky=tk.E+tk.S+tk.N)
		letter_M = tk.Label(namefr, text="M", font=("Courier", 14, "bold"), foreground="green")
		letter_M.grid(column=0, row=1, sticky=tk.E+tk.S+tk.N)
		rest_M = tk.Label(namefr, text="anage", font=("Courier", 14), foreground="green")
		rest_M.grid(column=1, row=1, sticky=tk.W+tk.S+tk.N)
		letter_R = tk.Label(namefr, text="R", font=("Courier", 14, "bold"), foreground="darkorange")
		letter_R.grid(column=0, row=2, sticky=tk.E+tk.S+tk.N)
		rest_R = tk.Label(namefr, text="adio-accumulation", font=("Courier", 14), foreground="darkorange")
		rest_R.grid(column=1, row=2, sticky=tk.W+tk.S+tk.N)
		letter_A = tk.Label(namefr, text="A", font=("Courier", 14, "bold"), foreground="purple")
		letter_A.grid(column=0, row=3, sticky=tk.E+tk.S+tk.N)
		rest_A = tk.Label(namefr, text="ssays", font=("Courier", 14), foreground="purple")
		rest_A.grid(column=1, row=3, sticky=tk.W+tk.S+tk.N)

		np_butt = ttk.Button(self.root, text="New Experiment", command=self.new_experiment)
		np_butt.pack(pady=(25, 0))

		bp_butt = ttk.Button(self.root, text="Browse Experiments", command=self.browse_experiments)
		bp_butt.pack(pady=(25, 0))
	
		nt_butt = ttk.Button(self.root, text="New Template", command=self.new_template)
		nt_butt.pack(pady=(25, 0))
	
		bt_butt = ttk.Button(self.root, text="Browse Templates", command=self.browse_templates)
		bt_butt.pack(pady=(25, 0))

		cf_butt = ttk.Button(self.root, text="Configure", command=self.configure)
		cf_butt.pack(pady=25)
		
		self.root.mainloop()	
	
	def new_experiment(self):
		window = NewExperimentWizard(self.app)
		window.title("New Experiment")
		window.resizable(False, False)

	def new_template(self):
		window = NewExperimentWizard(self.app, is_template=True)
		window.title("New Template")	
		window.resizable(False, False)

	def browse_experiments(self):
		window = tk.Toplevel(self.root)
		window.title("Browse Experiments")
		window.resizable(False, False)

		page_container = ExperimentBrowser(window, self.app)
		page_container.pack()

	def browse_templates(self):
		window = tk.Toplevel(self.root)
		window.title("Browse Templates")
		window.resizable(False, False)

		page_container = ExperimentBrowser(window, self.app, is_temp=True)
		page_container.pack()

	def configure(self):
		window = tk.Toplevel(self.root)
		window.title("Configure")
		window.resizable(False, False)

		frame = Configure(window, self.app)
		frame.pack()
		...


if __name__ == "__main__":
	g = GUI()


