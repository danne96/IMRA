def select_models(app, mod_sel_row):
	'''
	Update which models will be used to fit the current experiment data. Triggers when the user
	selects or deselects a model row on the wizard page 3.
	'''
	app.xpr.models[mod_sel_row.name] = mod_sel_row.checkvar.get()