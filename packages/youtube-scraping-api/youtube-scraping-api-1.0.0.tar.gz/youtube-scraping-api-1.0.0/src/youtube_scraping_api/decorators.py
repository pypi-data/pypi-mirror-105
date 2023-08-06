def logException(*outer_args):
	def check(*args, **kwargs):
		try: 
			return outer_args[-1](*args, **kwargs)
		except Exception as e:
			raise RuntimeError
	return check