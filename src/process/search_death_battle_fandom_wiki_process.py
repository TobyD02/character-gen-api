from typing import Any, Union

import requests
from bs4 import BeautifulSoup

from src.model.death_battle_fandom_query_response_model import DeathBattleFandomQueryResponseModel
from src.process.process_abstract import ProcessAbstract


class SearchDeathBattleFandomWikiProcess(ProcessAbstract):
    def __init__(self):
        self.base_url_template = "https://vsbattles.fandom.com/api.php?ction=query&format=json&generator=search&gsrsearch={character_name}&gsrlimit=3&prop=categories|pageimages&cllimit=max&pithumbsize=400&pilimit=max"
        self.base_url_template_page_id = "https://vsbattles.fandom.com/api.php?action=query&format=json&pageids={page_id}&prop=categories|pageimages&cllimit=max&pithumbsize=400&pilimit=max"

    def execute(self, character_name: str) -> list[DeathBattleFandomQueryResponseModel]:
        response = requests.post(
            self.base_url_template.format(character_name=character_name),
            timeout=10
        )

        search_results = response.json()["query"]["pages"]

        filtered = []

        # FIX 1: Use .values() to loop over the data dictionaries instead of the ID keys
        for page_data in search_results.values():
            # FIX 2: Use .get() to return an empty list if the page has zero categories
            categories = page_data.get("categories", [])

            # Count how many match our target filter
            has_character_tag = any(item["title"] == "Category:Characters" for item in categories)

            if has_character_tag:
                filtered.append(
                    DeathBattleFandomQueryResponseModel(
                        page_id=page_data["pageid"],
                        name=page_data["title"],
                        image_url=page_data["thumbnail"]["source"],
                        categories=[i["title"].lower().replace("category:", "").replace(" ", "_") for i in categories]
                    )
                )

        return filtered


    def execute_from_page_id(self, page_id: int):
        response = requests.post(
            self.base_url_template_page_id.format(page_id=page_id),
            timeout=10
        )

        search_results = response.json()["query"]["pages"]

        filtered = []

        # FIX 1: Use .values() to loop over the data dictionaries instead of the ID keys
        for page_data in search_results.values():
            # FIX 2: Use .get() to return an empty list if the page has zero categories
            categories = page_data.get("categories", [])

            # Count how many match our target filter
            has_character_tag = any(item["title"] == "Category:Characters" for item in categories)

            if has_character_tag:
                filtered.append(
                    DeathBattleFandomQueryResponseModel(
                        page_id=page_data["pageid"],
                        name=page_data["title"],
                        image_url=page_data["thumbnail"]["source"],
                        categories=[i["title"].lower().replace("category:", "").replace(" ", "_") for i in categories]
                    )
                )

        return filtered[0]
