import os
from pathlib import Path

from src.model.character_profile_model import CharacterProfileModel
from src.repository.repository_abstract import RepositoryAbstract


class CharacterProfileRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character_profile")

    def insert(self, character: CharacterProfileModel):
        self.cursor.execute("""
            INSERT INTO character_profile (
                character_id,
                image_url,
                description,
                powerscale_id,
                colour_primary,
                colour_secondary,
                colour_tertiary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING character_profile_id
            """, (
                character.character_id,
                character.image_url,
                character.description,
                character.powerscale_id,
                character.colour_primary,
                character.colour_secondary,
                character.colour_tertiary
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
