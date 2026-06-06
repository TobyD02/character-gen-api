import os
from pathlib import Path

from src.model.character_profile_model import CharacterProfileModel
from src.repository.repository_abstract import RepositoryAbstract


class CharacterProfileRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character_profile")

    def insert(self, character: CharacterProfileModel, powerscale_id: int):
        self.cursor.execute("""
            INSERT INTO character_profile (
                character_id,
                image,
                description,
                powerscale_id,
                html_colour_hex
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING character_profile_id
            """, (
                character.character_id,
                character.image_url,
                character.description,
                powerscale_id,
                character.html_colour_hex
            ))

        self.connection.commit()
        return self.cursor.fetchone()["character_profile_id"]

    def _build_character_model(self, row_data: dict):
        row_data["image_url"] = row_data.pop("image")
        row_data["categories"] = []
        row_data["special_abilities"] = []
        row_data["powerscale"] = None

        return CharacterProfileModel.model_validate(row_data)

    def select_by_id(self, id: int):
        self.cursor.execute("""
            SELECT character_profile_id
            FROM character_profile
            WHERE character_profile_id = %s
            """, (id,))
        row = self.cursor.fetchone()
        return row if row else None
