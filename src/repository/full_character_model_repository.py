from src.model.character_response_model import CharacterResponseModel
from src.model.character_model import CharacterModel
from src.model.ollama_character_model import OllamaSpecialAbilityModel
from src.model.character_profile_model import CharacterProfileModel
from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.repository.repository_abstract import RepositoryAbstract


class FullCharacterModelRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__()

    def select(self, character: CharacterModel) -> CharacterResponseModel:
        self.cursor.execute(
            """
            SELECT *
            FROM character_profile
            WHERE character_id = %s
            """, (character.character_id,))

        cp = self.cursor.fetchone()

        print("Got Profile", flush=True)
        character_profile = CharacterProfileModel.model_validate(cp)
        print(f"Populated Profile {character_profile}", flush=True)

        self.cursor.execute(
            """
            SELECT c.category_id,
                   c.name
            FROM character_category cc
                     JOIN category c
                          ON c.category_id = cc.category_id
            WHERE cc.character_id = %s
            """, (character.character_id,)
        )

        print("Got Categories", flush=True)
        categories = [r["name"] for r in self.cursor.fetchall()]
        print(f"Populated Categories {categories}", flush=True)


        self.cursor.execute(
            """
            SELECT *
            FROM powerscale
            WHERE powerscale_id = %s
            """, (character_profile.powerscale_id, ))

        ps = self.cursor.fetchone()
        print("Got Powerscale", flush=True)
        powerscale = CharacterPowerScaleModel.model_validate(ps)
        print(f"Populated Powerscale {powerscale}", flush=True)

        self.cursor.execute(
            """
            SELECT * FROM character_special_ability
            WHERE character_id = %s
            """, (character_profile.character_id,)
        )

        csa = self.cursor.fetchall()
        print("Got Special Abilities", flush=True)
        special_abilities = [OllamaSpecialAbilityModel.model_validate(i) for i in csa]
        print(f"Populated Special Abilities {special_abilities}", flush=True)

        return CharacterResponseModel(
            character=character,
            character_profile=character_profile,
            powerscale=powerscale,
            special_abilities=special_abilities,
            categories=categories,
        )
