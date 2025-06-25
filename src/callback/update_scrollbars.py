import tkinter as tk

def update_scrollbars(sframe):
	'''
	When the contents of a scrollable frame is updated, check whether  
	'''
	sframe.canvas.update_idletasks()
	if sframe.canvas.winfo_height() < sframe.contents.winfo_reqheight():
		sframe.vbar.grid(column=2, row=1, sticky=tk.N+tk.S)
	else:
		sframe.vbar.grid_remove()
	if sframe.canvas.winfo_reqwidth() < sframe.contents.winfo_width():
		sframe.hbar.grid(column=1, row=2, sticky=tk.W+tk.E)
	else:
		sframe.hbar.grid_remove()