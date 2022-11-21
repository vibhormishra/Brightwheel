class Util(object):

	@staticmethod
	def validate_input_post_request(input_data: dict)-> bool:
		if ('id' not in input_data or 'readings' not in input_data
		    or ('readings' in input_data and len(input_data['readings']) == 0)):
		    return False

		for reading in input_data['readings']:
			if 'timestamp' not in reading or 'count' not in reading:
				return False

		return True
