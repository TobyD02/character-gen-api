import requests

MAX_CHARACTERS = 33625

for i in range(1, MAX_CHARACTERS + 1):
    response = requests.get(f"http://localhost/character/{i}")
    if response.status_code != 200:
        print(f"Error: index {i} | {response.status_code} ")
    else:
        print(f"Generated index {i}")