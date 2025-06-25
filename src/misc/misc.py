CELL_LINE_VBAR = {"BY-2":	3.53E-14,
			  	  "BY-2H":	3.53E-14,
			  	  "VBI-0":	3.65E-14,
			  	  "VBI-2b":	6.08E-14,
			 	  }

def alphabet_labels(start, end):
	return [number_to_alphabet_label(i) for i in range(start, end+1)]
def number_to_alphabet_label(n):
	result = []
	
	while n > 0:
		n, rem = divmod(n - 1, 26)
		result.append("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[rem])
	
	return ''.join(reversed(result))

def shorten_path(text, max_width=50, start=9):
	if len(text) > max_width:
		return f"{text[:start]}...{text[-max_width + 2 + start:]}"
	return text