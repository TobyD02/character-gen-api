from src.model.ollama_character_model import OllamaSpecialAbilityModel
from src.repository.repository_abstract import RepositoryAbstract
from src.model.character_profile_model import CharacterProfileModel


class CharacterSpecialAbilityRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character_special_ability")

    def insert_character_special_abilities(self, character_id: int, special_abilities: list[OllamaSpecialAbilityModel]):
        self.cursor.executemany(
            """
            INSERT INTO character_special_ability (character_id, name, description, special_ability_emoji)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (character_id, name) DO NOTHING
            """, [
                (character_id, a.name, a.description, a.special_ability_emoji) for a in
                special_abilities
            ])

        self.connection.commit()
