from flask import Flask, url_for, request
import json
from data import DeviceData
from error import Error
import traceback
from util import Util

ERROR_DEVICE_ID_NOT_FOUND = "Device_id not found"
ERROR_INVALID_PARAMETER = "Invalid parameter"
EEROR_INVALID_INPUT = "Invalid input"
ERROR_CONTENT_TYPE_NOT_SUPPORTED = 'Content-Type not supported!'
GENERIC_ERROR = "Something went wrong"

api = Flask(__name__)
data = DeviceData()


@api.route('/device/readings', methods=['POST'])
def store_readings():
  content_type = request.headers.get('Content-Type')
  input_data = {}
  if (content_type == 'application/json'):
    input_data = request.json    
  else:
    return Error(ERROR_CONTENT_TYPE_NOT_SUPPORTED).get_json()

  if not Util.validate_input_post_request(input_data):
    return Error(EEROR_INVALID_INPUT).get_json()

  try:
    data.store_readings(input_data['id'], input_data['readings'])
  except Exception as err:
    traceback.print_exc()    
    return Error(GENERIC_ERROR).get_json()

  return json.dumps({'operation':'success'})


@api.route('/device/get/timestamp', methods=['GET'])
def get_latest_timestamp():
  args = request.args
  device_id = args.get('id')
  if device_id is None:
    return Error(ERROR_INVALID_PARAMETER).get_json()

  ts = data.get_latest_timestamp(device_id)
  if ts:
    return json.dumps({'latest_timestamp':ts})
  else:    
    return Error(ERROR_DEVICE_ID_NOT_FOUND).get_json()

@api.route('/device/get/count', methods=['GET'])
def get_cumulative_count():
  args = request.args
  device_id = args.get('id')
  if device_id is None:
    return Error(ERROR_INVALID_PARAMETER).get_json()

  count = data.get_cumulative_count(device_id)
  if count is None:    
    return Error(ERROR_DEVICE_ID_NOT_FOUND).get_json()
  else:    
    return json.dumps({'cumulative_count':count})

if __name__ == '__main__':    
  api.run()