from src.model.character_special_ability_model import CharacterSpecialAbilityModel
from src.repository.repository_abstract import RepositoryAbstract


class CharacterSpecialAbilityRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character_special_ability")

    def insert_character_special_abilities(
        self, character_id: int, special_abilities: list[CharacterSpecialAbilityModel],
    ):
        self.cursor.executemany(
            """
            INSERT INTO character_special_ability (character_id, name, description, target, range, area_of_effect,
                                                   health_add, defense_add, movement_add, attack_power_add, will_stun,
                                                   cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (character_id, name) DO NOTHING
            """, [
                (character_id, a.name, a.description, a.target, a.range, a.area_of_effect, a.health_add, a.defense_add,
                 a.movement_add, a.attack_power_add, a.will_stun, a.cost) for a in
                special_abilities
            ])

        self.connection.commit()
