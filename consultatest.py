

import json
import requests


url = "http://192.168.1.30:5000/tarea?worker=1"
response = requests.get(url)
data = json.loads(response.content.decode())
print (data)



