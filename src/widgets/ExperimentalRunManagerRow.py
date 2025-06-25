import tkinter as tk
from tkinter import ttk

from ..callback.experimental_run_manager import *
from ..session import Session

class ExperimentalRunManagerRow(ttk.Frame):
	def __init__(self, container, app: Session, samp_count, samp_vol, radio_conc, cond_label=None, *args, **kwargs):
		super().__init__(container.contents, *args, **kwargs)		
		# Container is a scrollable frame !
		widths = [70, 100, 100, 100, 100, 130]
		frames = []
		for width in widths:
			frame = ttk.Frame(self, width=width, height=39)
			frame.pack_propagate(False)
			frame.pack(side="left")
			frames.append(frame)
		
		self.num = len(container.contents.winfo_children())
		self.run_num = ttk.Label(frames[0], text=f"{self.num:02d}")
		self.run_num.pack(side="left", padx=(5, 0))
		
		conds = app.xpr.conds			
		self.cond = ttk.Combobox(frames[1], values=list(conds.keys()), width=4)
		if cond_label:
			self.cond.set(cond_label)
		#self.cond.bind("<<ComboboxSelected>>", lambda e: update_row_in_run_manager(container, app, self))
		self.cond.bind("<FocusOut>", lambda e: update_row_in_run_manager(container, app, self))
		self.cond.pack(side="left", padx=(5, 0))
		
		self.samps_var = tk.StringVar(value=samp_count)
		self.samps = ttk.Entry(frames[2], width=4, textvariable=self.samps_var)
		self.samps.bind("<FocusOut>", lambda e: update_sample_count(app, self))
		self.samps.pack(side="left", padx=(5, 0))
		
		self.svol_var = tk.StringVar(value=samp_vol)
		self.svol = ttk.Entry(frames[3], width=6, textvariable=self.svol_var)
		self.svol.bind("<FocusOut>", lambda e: update_sample_volume(app, self))
		self.svol.pack(side="left", padx=(5, 0))
		
		self.radio_c_var = tk.StringVar(value=radio_conc)
		self.radio_c = ttk.Entry(frames[4], width=4, textvariable=self.radio_c_var)
		self.radio_c.bind("<FocusOut>", lambda e: update_tracer_concentration(app, self))
		self.radio_c.pack(side="left", padx=(5, 0))
		
		delbtn = ttk.Button(frames[5], text="Delete", command=lambda: remove_row_from_run_manager(container, app, self))
		delbtn.pack(side="left", padx=(5, 0))
