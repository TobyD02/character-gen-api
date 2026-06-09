import requests
import json
JSON_FILE_LOCATION = "../json_dump.json"

response = requests.get("http://localhost/api/characters/all")
json_data = response.json()

with open(JSON_FILE_LOCATION, "w") as f:
    json.dump(json_data, f)