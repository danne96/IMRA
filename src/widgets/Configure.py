from tkinter import ttk
import tkinter as tk

from ..callback.configure import *
from ..misc.misc import shorten_path
from ..session import Session

class Configure(ttk.Frame):
    def __init__(self, container, app: Session, label_max_width: int = 50, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        dfr = ttk.Frame(self)
        dfr.grid(row=0, column=0, padx=15, pady=10, sticky=tk.W+tk.E)

        dfr_title = ttk.Label(dfr, text="Edit default directories", font="TkDefaultFont 10 bold")
        dfr_title.grid(row=0, column=0, columnspan=3, sticky=tk.W)

        r_dir_label = ttk.Label(dfr, text="Radio-sheet directory:")
        r_dir_label.grid(row=1, column=0, pady=10, sticky=tk.W)
        r_dir_path = ttk.Label(dfr, text=shorten_path(app.config["radio_sheet_dir"]), width=label_max_width)
        r_dir_path.grid(row=1, column=1, padx=5, pady=10, sticky=tk.W)
        r_dir_butt = ttk.Button(dfr, text="Change")
        r_dir_butt.grid(row=1, column=2, pady=10, sticky=tk.W)
        r_dir_butt.configure(command=lambda: select_radiosheet_dir(container, app, app.config["radio_sheet_dir"], r_dir_path, label_max_width))

        e_dir_label = ttk.Label(dfr, text="Experiment JSON directory:")
        e_dir_label.grid(row=2, column=0, pady=10, sticky=tk.W)
        e_dir_path = ttk.Label(dfr, text=shorten_path(app.config["experiment_dir"]), width=label_max_width)
        e_dir_path.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)
        e_dir_butt = ttk.Button(dfr, text="Change")
        e_dir_butt.grid(row=2, column=2, pady=10, sticky=tk.W)
        e_dir_butt.configure(command=lambda: select_experiment_dir(container, app, app.config["experiment_dir"], e_dir_path, label_max_width))

        t_dir_label = ttk.Label(dfr, text="Template JSON directory:")
        t_dir_label.grid(row=3, column=0, pady=10, sticky=tk.W)
        t_dir_path = ttk.Label(dfr, text=shorten_path(app.config["template_dir"]), width=label_max_width)
        t_dir_path.grid(row=3, column=1, padx=5, pady=10, sticky=tk.W)
        t_dir_butt = ttk.Button(dfr, text="Change")
        t_dir_butt.grid(row=3, column=2, pady=10, sticky=tk.W)
        t_dir_butt.configure(command=lambda: select_template_dir(container, app, app.config["template_dir"], t_dir_path, label_max_width))

        o_dir_label = ttk.Label(dfr, text="Default XLSX output directory:")
        o_dir_label.grid(row=4, column=0, pady=10, sticky=tk.W)
        o_dir_path = ttk.Label(dfr, text=shorten_path(app.config["default_output_dir"]), width=label_max_width)
        o_dir_path.grid(row=4, column=1, padx=5, pady=10, sticky=tk.W)
        o_dir_butt = ttk.Button(dfr, text="Change")
        o_dir_butt.grid(row=4, column=2, pady=10, sticky=tk.W)
        o_dir_butt.configure(command=lambda: select_default_output_dir(container, app, app.config["default_output_dir"], o_dir_path, label_max_width))

        nfr = ttk.Frame(self)
        nfr.grid(row=1, column=0, padx=15, pady=10, sticky=tk.W+tk.E)
        nfr.grid_columnconfigure(0, weight=1) ## this must be here for the frame to fully spread

        can_btn = ttk.Button(nfr, text="Cancel")
        can_btn.grid(row=0, column=0, sticky=tk.W)
        can_btn.config(command=container.destroy)

        sav_btn = ttk.Button(nfr, text="Save")
        sav_btn.grid(row=0, column=1, sticky=tk.E)
        sav_btn.config(command=lambda: save_configuration(container, app))
