import enum
from pydantic import BaseModel

class OllamaSpecialAbilityModel(BaseModel):
    name: str
    description: str
    special_ability_emoji: str

class OllamaCharacterDefinitionModel(BaseModel):
    name: str
    description: str
    special_ability_1: OllamaSpecialAbilityModel
    special_ability_2: OllamaSpecialAbilityModel
    special_ability_3: OllamaSpecialAbilityModel
    special_ability_4: OllamaSpecialAbilityModel
    html_colour_hex: str
