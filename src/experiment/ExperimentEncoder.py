import json
import numpy as np

class ExperimentEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, np.integer):
			return int(o)
		if isinstance(o, np.floating):
			return int(o)
		if isinstance(o, np.ndarray):
			return o.tolist()
		return super(ExperimentEncoder, self).default(o)