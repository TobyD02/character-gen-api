import os
import sqlite3

from src.model.character_profile_model import CharacterProfileModel
from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.repository.repository_abstract import RepositoryAbstract


class FullCharacterModelRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__()

    def select(self, character_id: int) -> CharacterProfileModel:
        self.cursor.execute("""
                            SELECT *
                            FROM character_profile
                            WHERE character_id = %s
                            """, (character_id))

        character = self.cursor.fetchone()
        if not character:
            return None

        character = dict(character)

        self.cursor.execute("""
                            SELECT category
                            FROM character_category
                            WHERE character_id = :id
                            """, {"id": character_id})

        categories = [r["category"] for r in self.cursor.fetchall()]

        self.cursor.execute("""
                            SELECT tier, label, name
                            FROM powerscale
                            WHERE id = :id
                            """, {"id": character["powerscale_id"]})

        ps = self.cursor.fetchone()
        ps = dict(ps)
        powerscale = CharacterPowerScaleModel(
            tier=ps["tier"],
            label=ps["label"],
            name=ps["name"],
        )

        return CharacterProfileModel(
            id=character["id"],
            page_id=character["page_id"],
            name=character["name"],
            image_url=character["image"],
            categories=categories,
            description=character["description"] or "",
            special_abilities=[],
            powerscale=powerscale,
            html_colour_hex=character["html_colour_hex"],
        )
