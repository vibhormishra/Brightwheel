# Brightwheel


## How to run this locally

1) The code is using Flask library in Python to host a server locally with the endpoints. The flask can be installed using this command: ```pip install flask```
2) Now to start up the server, run this command: ```python <local_path_to_this_file>\python_flask_api.py```
3) These APIs were tested using Postman and can be accessed using following urls locally:
  a) http://127.0.0.1:5000/device/readings - POST request 
    i) it requires ```"Content-Type":"application/json"``` in request header
  b) http://localhost:5000/device/get/count?id=36d5658a-6908-479e-887e-a949ec199272
  c) http://127.0.0.1:5000/device/get/timestamp?id=36d5658a-6908-479e-887e-a949ec199272
  
## Code Structure
- The file that has the ```main``` function is ```python_flask_api.py```. This file defines all three endpoints: ```device/readings```, ```device/get/count```, ```device/get/timestamp```.
- The ```data.py``` file has ```DeviceData``` class that defines methods for storing readings and fetching latest timestamp and count for each device.
- The ```error.py``` file has ```Error``` class.
- The ```util.py``` file has ```Util``` class that defines basic util functions like validating input for POST request.
  
## Algorithm

### Data Structure
1) To store different device-ids and their timestamps and counts, using ```Dictionary``` (quivalent to HashMap in JAVA) so that device properties can be efficiently retrieved.
2) To keep latest timestamp and also to make sure we ignore duplicate timestamps for a device, using ```set``` in Python. A set can hold only unique values, thus serves our purpose of keeping timestamps unique.

### Psuedo code

1. For any request to store data:
   - check if the input has required fields and if not, return **Invalid input error**
   - retrieve timestamp set(```ts_set```), latest timestamp string (```cache_ts```) and count (```cache_count```) for a device map dictionary(```deviceMap```). If device id doesn't exist, initalize these values with empty set, empty string and 0 count.
   - Iterate through all the readings in the request:
   - if the new timestamp from the reading is greater than the cache_ts, replace ```cache_ts``` with new higher value
   - if the new timestamp is not in the ```ts_set``` i.e. it's not seen before, add new count to ```cache_count``` and this timestamp to ```ts_set```. Otherwise don't add the count.
   - update the ```deviceMap``` with new ```cache_count```, ```cache_ts``` and updated ```ts_set```.
  
2) For retrieving latest timestamp for a device id:
   - check if device id is supplied as part of GET request
   - check if device id exists in device map dictionary(```deviceMap```) and return the value in constant ```O(1)``` time. 

## Improvements 
Wanted to improve the APIs further in the following ways:
1. create data contract for the fields expected in the input for POST request and add validation for them using decorator so that explicit request input validation can be avoided for each API
2. use better framework (JAVA based) that supports creating classes for each API. Had to resort to use Flask for quick implementation as I am most familiar and quick with Python data structures and implementation.
3. On data structure side, in current implementation ```set()``` that stores all unique timestamps for a device is forever increasing. Pruning it on regular intervals would save on space in cache. 
4. Include logging for any future issue debugging, to a log file using Python logging framework.
