import time

import requests
from src.repository.character_repository import CharacterRepository

character_repository = CharacterRepository()

API_URL = "https://vsbattles.fandom.com/api.php"


def fetch_category_members(cmcontinue=None):
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:Characters",
        "cmlimit": "max",
        "format": "json",
    }

    if cmcontinue:
        params["cmcontinue"] = cmcontinue

    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()


def ingest_all_characters():
    cmcontinue = None

    while True:
        data = fetch_category_members(cmcontinue)

        members = data["query"]["categorymembers"]

        for member in members:
            page_id = member["pageid"]
            name = member["title"]

            character_repository.insert(page_id, name)

        cmcontinue = data.get("continue", {}).get("cmcontinue")

        if not cmcontinue:
            break


        print(f"inserted {len(members)}")
        time.sleep(0.5)


if __name__ == "__main__":
    ingest_all_characters()
