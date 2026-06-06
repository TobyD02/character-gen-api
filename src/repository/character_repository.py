import os
from pathlib import Path

from src.model.character_profile_model import CharacterProfileModel
from src.repository.repository_abstract import RepositoryAbstract


class CharacterRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character")

    def insert(self, character: CharacterProfileModel, powerscale_id: int):
        self.cursor.execute(
            """
            INSERT INTO character_profile (page_id,
                                           name,
                                           image,
                                           description,
                                           powerscale_id,
                                           html_colour_hex)
            VALUES (:page_id,
                    :name,
                    :image,
                    :description,
                    :powerscale_id,
                    :html_colour_hex)
            """, {
                "page_id": character.page_id,
                "name": character.name,
                "image": character.image_url,
                "description": character.description,
                "powerscale_id": powerscale_id,
                "html_colour_hex": character.html_colour_hex
            })

        self.connection.commit()
        return self.cursor.lastrowid

    def _build_character_model(self, row_data: dict):
        row_data["image_url"] = row_data.pop("image")
        row_data["categories"] = []
        row_data["special_abilities"] = []
        row_data["powerscale"] = None

        return CharacterProfileModel.model_validate(row_data)

    def select_by_id(self, id: int) -> int | None:
        self.cursor.execute(
            """
            SELECT *
            FROM character_profile
            WHERE id = :id
            """,
            {"id": id}
        )

        row = self.cursor.fetchone()
        if row is None:
            return None

        return row["id"]


    def select_by_name(self, name: str) -> int | None:
        self.cursor.execute(
            """
            SELECT id
            FROM character_profile
            WHERE name = :name
            """,
            {"name": name}
        )

        row = self.cursor.fetchone()
        if row is None:
            return None

        return row["id"]


    def select_by_page_id(self, page_id: int) -> int | None:
        self.cursor.execute(
            """
            SELECT id
            FROM character_profile
            WHERE page_id = :page_id
            """,
            {"page_id": page_id}
        )

        row = self.cursor.fetchone()
        if row is None:
            return None

        return row["id"]
