import tkinter as tk
from tkinter import ttk

from ..callback.update_scrollbars import update_scrollbars

class ScrollableFrame(ttk.Frame):
	def __init__(self, container, vertical_increment=False, horizontal_increment=False, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		
		# Default TFrame background for canvases
		default_bg = ttk.Style().lookup("TFrame", "background")
		# Explicit style settings for all scrollbars
		ttk.Style().configure("TScrollbar", width=14, borderwidth=1)
				
		# These frames serve to fill the "dead space" when scrollbars are created
		ttk.Frame(self, borderwidth=1.2, relief="raised").grid(column=2, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
		ttk.Frame(self, borderwidth=1.2, relief="raised").grid(column=0, row=2, sticky=tk.W+tk.N+tk.E+tk.S)
		ttk.Frame(self, borderwidth=1.2, relief="raised").grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
		ttk.Frame(self, borderwidth=1.2, relief="groove").grid(column=2, row=2, sticky=tk.NE)
		
		if horizontal_increment:
			self.hbar_frame = ttk.Frame(self, height=16)
			self.hbar_frame.grid(column=1, row=2)
		if vertical_increment:
			self.vbar_frame = ttk.Frame(self, width=16)
			self.vbar_frame.grid(column=2, row=1)
		
		# Create a header for optional column names
		self.col_head_canvas = tk.Canvas(self, bg=default_bg, highlightthickness=0)
		self.col_head = ttk.Frame(self.col_head_canvas)
		self.col_head.bind("<Configure>", lambda e: self.col_head_canvas.config(scrollregion=self.col_head_canvas.bbox("all")))
		
		# Create a header for optional row names
		self.row_head_canvas = tk.Canvas(self, bg=default_bg, highlightthickness=0)
		self.row_head = ttk.Frame(self.row_head_canvas)
		self.row_head.bind("<Configure>", lambda e: self.row_head_canvas.config(scrollregion=self.row_head_canvas.bbox("all")))

		# Create a canvas to hold the scrollable contents
		self.canvas = tk.Canvas(self, bg=default_bg, highlightthickness=0)
		self.canvas.grid(column=1, row=1, sticky=tk.NSEW)
		
		# Create the scrollbars
		self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.ver_scrollfun)
		self.hbar = ttk.Scrollbar(self, orient="horizontal", command=self.hor_scrollfun)
		self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
		self.col_head_canvas.configure(xscrollcommand=self.hbar.set)
		self.row_head_canvas.configure(yscrollcommand=self.vbar.set)
		
		# Create the scrollable frame capable to hold further contents
		self.contents = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.contents, anchor="nw")
		self.contents.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
		
		# Create a shortcut so that children of the contents frame can
		# easily refer to the scrollable frame
		self.contents.sframe = self
		
		update_scrollbars(self)
	
	def create_col_head(self, width=None, height=None):
		if not width:
			width = self.canvas.winfo_width()
		if not height:
			self.col_head.update()
			height = self.col_head.winfo_reqheight()
		self.col_head_canvas.config(width=width, height=height)	
		self.col_head_canvas.grid(column=1, row=0, sticky=tk.NSEW)
		self.col_head_canvas.create_window((0, 0), window=self.col_head, anchor="nw")
	
	def create_row_head(self, width=None, height=None):
		if not width:
			self.row_head.update()
			width = self.row_head.winfo_reqwidth()
		if not height:
			height = self.canvas.winfo_height()
		self.row_head_canvas.config(width=width, height=height)
		self.row_head_canvas.grid(column=0, row=1, sticky=tk.NSEW)
		self.row_head_canvas.create_window((0, 0), window=self.row_head, anchor="nw")

	
	def ver_scrollfun(self, *args):
		self.canvas.yview(*args)
		self.row_head_canvas.yview(*args)
		
	def hor_scrollfun(self, *args):
		self.canvas.xview(*args)
		self.col_head_canvas.xview(*args)
