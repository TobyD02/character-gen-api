from pydantic import BaseModel

from src.model.character_special_ability_model import CharacterSpecialAbilityModel
from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.model.character_model import CharacterModel
from src.model.character_profile_model import CharacterProfileModel

class CharacterResponseModel(BaseModel):
    character: CharacterModel
    character_profile: CharacterProfileModel
    special_abilities: list[CharacterSpecialAbilityModel]
    categories: list[str]
    powerscale: CharacterPowerScaleModel

