import json 

class Error:
	def __init__(self, error_str: str):
		self.error_str = error_str

	def get_json(self) -> dict:
		return json.dumps({'error':self.error_str})