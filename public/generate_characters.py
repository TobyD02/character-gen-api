import requests

MAX_CHARACTERS = 33625
START_CHARACTER_INDEX = 1973


for i in range(START_CHARACTER_INDEX, MAX_CHARACTERS + 1):
    response = requests.get(f"http://localhost/api/character/{i}")
    if response.status_code != 200:
        print(f"Error: index {i} | {response.status_code} ")
    else:
        print(f"Generated index {i}")