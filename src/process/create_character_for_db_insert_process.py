from src.model import ollama_character_model
from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.model.character_profile_model import CharacterProfileModel
from src.model.ollama_character_model import OllamaCharacterDefinitionModel
from src.process.process_abstract import ProcessAbstract


class CreateCharacterForDbInsertProcess(ProcessAbstract):
    def __init__(self):
        pass

    # def execute(
    #     self,
    #     anilist_character_model: AnilistCharacterModel,
    #     ollama_character_definition_model: OllamaCharacterDefinitionModel
    # ) -> CharacterProfileModel:
    #     return CharacterProfileModel(
    #         anilist_id=anilist_character_model.id,
    #         name=anilist_character_model.name,
    #         image=anilist_character_model.image,
    #         description=anilist_character_model.description,
    #
    #         # Generated enrichment
    #         special_ability_name=ollama_character_definition_model.special_ability.name,
    #         special_ability_description=ollama_character_definition_model.special_ability.description,
    #         special_ability_emoji=ollama_character_definition_model.special_ability.special_ability_emoji,
    #         powerscale=ollama_character_definition_model.powerscale,
    #         html_colour_hex=ollama_character_definition_model.html_colour_hex,
    #     )

    def execute(self, name: str, image_url: str, powerscaling: CharacterPowerScaleModel, page_id: int, categories: list[str], ollama_character_definition_model: OllamaCharacterDefinitionModel):
        return CharacterProfileModel(
            page_id=page_id,
            name=name,
            image_url=image_url,
            categories=categories,
            description=ollama_character_definition_model.description,
            # Generated enrichment
            special_abilities=[
                ollama_character_definition_model.special_ability_1,
                ollama_character_definition_model.special_ability_2,
                ollama_character_definition_model.special_ability_3,
                ollama_character_definition_model.special_ability_4,
            ],
            powerscale=powerscaling,
            html_colour_hex=ollama_character_definition_model.html_colour_hex,
        )
