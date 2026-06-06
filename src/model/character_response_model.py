from pydantic import BaseModel

from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.model.ollama_character_model import OllamaSpecialAbilityModel
from src.model.character_model import CharacterModel
from src.model.character_profile_model import CharacterProfileModel


class CharacterResponseModel(BaseModel):
    character: CharacterModel
    character_profile: CharacterProfileModel
    special_abilities: list[OllamaSpecialAbilityModel]
    categories: list[str]
    powerscale: CharacterPowerScaleModel

