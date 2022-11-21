from collections import defaultdict
from typing import Optional
from datetime import datetime

class DeviceData:
	
	def __init__(self):
		self.deviceMap = defaultdict(lambda: (set, str, int))

	def store_readings(self, device_id: str, readings: Optional[dict]) -> None:
		
		# If device id is not found, create record for the device_id
		if device_id not in self.deviceMap:
			self.deviceMap[device_id] = (set(),'',0)


		# fetch set of timestamps, latest timestamp and cumulative count for all readings so far
		ts_set, cache_ts, cache_count = self.deviceMap[device_id]
		format_data = "%Y-%m-%dT%H:%M:%S%z"
		date_cache = None
		if len(cache_ts) > 0:
			date_cache = datetime.strptime(cache_ts,format_data)
		for reading in readings:	
			ts = reading['timestamp']
			count = reading['count']
			date_new = datetime.strptime(ts, format_data)							
			if date_cache is None or (date_cache and date_new > date_cache):
				cache_ts = ts
				date_cache = date_new
			if ts not in ts_set:
				ts_set.add(ts)
				cache_count += count

		# Update cache data for this device now
		self.deviceMap[device_id] = (ts_set, cache_ts, cache_count)
			
	def get_latest_timestamp(self, device_id: str) -> Optional[str]:
		if device_id in self.deviceMap:
			return self.deviceMap[device_id][1]
		else:
			return None

	def get_cumulative_count(self, device_id: str) -> Optional[int]:
		if device_id in self.deviceMap:
			return self.deviceMap[device_id][2]		
		else:
			return None