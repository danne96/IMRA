from tkinter import filedialog as fd
from tkinter import ttk
import json

from ..misc.misc import shorten_path

def select_radiosheet_dir(win, app, initialdir, label: ttk.Label, max_width):
    new_dir = fd.askdirectory(initialdir=initialdir, parent=win)
    if new_dir:
        app.config["radio_sheet_dir"] = new_dir
        label.config(text=shorten_path(new_dir, max_width=max_width))

def select_experiment_dir(win, app, initialdir, label: ttk.Label, max_width):
    new_dir = fd.askdirectory(initialdir=initialdir, parent=win)
    if new_dir:
        app.config["experiment_dir"] = new_dir
        label.config(text=shorten_path(new_dir, max_width=max_width))

def select_template_dir(win, app, initialdir, label: ttk.Label, max_width):
    new_dir = fd.askdirectory(initialdir=initialdir, parent=win)
    if new_dir:
        app.config["template_dir"] = new_dir
        label.config(text=shorten_path(new_dir, max_width=max_width))

def select_default_output_dir(win, app, initialdir, label: ttk.Label, max_width):
    new_dir = fd.askdirectory(initialdir=initialdir, parent=win)
    if new_dir:
        app.config["default_output_dir"] = new_dir
        label.config(text=shorten_path(new_dir, max_width=max_width))

def save_configuration(win, app):
    with open("config.json", "w") as out:
        json.dump(app.config, out, indent=4)
    win.destroy()
