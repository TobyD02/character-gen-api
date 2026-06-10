from src.model.character_response_model import CharacterResponseModel
from src.model.character_model import CharacterModel
from src.model.character_special_ability_model import CharacterSpecialAbilityModel
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

        character_profile = CharacterProfileModel.model_validate(cp)

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

        categories = [r["name"] for r in self.cursor.fetchall()]

        self.cursor.execute(
            """
            SELECT *
            FROM powerscale
            WHERE powerscale_id = %s
            """, (character_profile.powerscale_id,))

        ps = self.cursor.fetchone()
        powerscale = CharacterPowerScaleModel.model_validate(ps)

        self.cursor.execute(
            """
            SELECT *
            FROM character_special_ability
            WHERE character_id = %s
            """, (character_profile.character_id,)
        )

        csa = self.cursor.fetchall()
        special_abilities = [CharacterSpecialAbilityModel.model_validate(i) for i in csa]

        return CharacterResponseModel(
            character=character,
            character_profile=character_profile,
            powerscale=powerscale,
            special_abilities=special_abilities,
            categories=categories,
        )

    def select_all(self):
        self.cursor.execute(
            """
            SELECT json_build_object(
                           'character', row_to_json(c),
                           'character_profile', row_to_json(cp),
                           'powerscale', row_to_json(ps),

                           'categories',
                           (
                               SELECT json_agg(cat.name)
                               FROM character_category cc
                                        JOIN category cat
                                             ON cat.category_id = cc.category_id
                               WHERE cc.character_id = c.character_id
                           ),

                           'special_abilities',
                           (
                               SELECT json_agg(row_to_json(sa))
                               FROM character_special_ability sa
                               WHERE sa.character_id = c.character_id
                           )
                   ) as character
            FROM character c
                     JOIN character_profile cp
                          ON cp.character_id = c.character_id
                     JOIN powerscale ps
                          ON ps.powerscale_id = cp.powerscale_id;
            """)

        return [CharacterResponseModel.model_validate(i["character"]) for i in self.cursor.fetchall()]

    def select_all_scaled(self):
        self.cursor.execute(
            """
            SELECT json_build_object(
                           'character', row_to_json(c),
                           'character_profile', row_to_json(cp),
                           'powerscale', row_to_json(ps),

                           'categories',
                           (
                               SELECT json_agg(cat.name)
                               FROM character_category cc
                                        JOIN category cat
                                             ON cat.category_id = cc.category_id
                               WHERE cc.character_id = c.character_id
                           ),

                           'special_abilities',
                           (
                               SELECT json_agg(
                                              json_build_object(
                                                      'name', sa.name,
                                                      'description', sa.description,
                                                      'target', sa.target,

                                                      'range', (sa.range * POWER(ps.tier, 2))::int,
                                                      'area_of_effect', (sa.area_of_effect * POWER(ps.tier, 2))::int,
                                                      'health_add', (sa.health_add * POWER(ps.tier, 2))::int,
                                                      'defense_add', (sa.defense_add * POWER(ps.tier, 2))::int,
                                                      'movement_add', (sa.movement_add * POWER(ps.tier, 2))::int,
                                                      'attack_power_add', (sa.attack_power_add * POWER(ps.tier, 2))::int,
                                                      'will_stun', sa.will_stun,
                                                      'cost', (sa.cost * POWER(ps.tier, 2))::int
                                              )
                                      )
                               FROM character_special_ability sa
                               WHERE sa.character_id = c.character_id
                           )
                   ) AS character
            FROM character c
                     JOIN character_profile cp
                          ON cp.character_id = c.character_id
                     JOIN powerscale ps
                          ON ps.powerscale_id = cp.powerscale_id
            ORDER BY ps.tier DESC;
            """)

        return [CharacterResponseModel.model_validate(i["character"]) for i in self.cursor.fetchall()]
