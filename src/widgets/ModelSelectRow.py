import tkinter as tk
from tkinter import ttk

from ..callback.model_select_row import *

class ModelSelectRow(ttk.Frame):
	def __init__(self, container, app, name, display_name, desc, *args, **kwargs):
		super().__init__(container, *args, **kwargs)

		self.name = name
		self.checkvar = tk.IntVar()
		
		widths = [125, 575]
		frames = []
		for width in widths:
			frame = ttk.Frame(self, width=width, height=75)
			frame.pack_propagate(False)
			frame.pack(side="left")
			frames.append(frame)
		
		check = ttk.Checkbutton(frames[0], text=display_name, variable=self.checkvar,
							    command=lambda: select_models(app, self))
		check.pack(side="left", fill="y", padx=(5,0))
		
		if app.xpr.models[name]:
			self.checkvar.set(1)
		else:
			self.checkvar.set(0)
			
		ttk.Label(frames[1], text=desc).pack(side="left", padx=(5,0))

