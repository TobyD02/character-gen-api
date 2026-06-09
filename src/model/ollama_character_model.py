import enum
from typing import Union

from pydantic import BaseModel, Field, ConfigDict


class AbilityTarget(enum.Enum):
    SELF = "self"
    OTHER = "other"
    MULTI = "multi"

class AbilityTypeModel(enum.Enum):
    DEBUFF = "debuff"
    BUFF = "buff"


class OllamaSpecialAbilityModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: AbilityTypeModel

    name: str
    description: str
    target: AbilityTarget
    range: int = Field(..., ge=0, le=10)
    area_of_effect: int = Field(..., ge=0, le=10)

    health_impact_factor: int = Field(ge=0, le=10)
    defense_impact_factor: int = Field(ge=0, le=10)
    movement_impact_factor: int = Field(ge=0, le=10)
    attack_power_impact_factor: int = Field(ge=0, le=10)
    will_stun: bool

class OllamaCharacterDefinitionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    character_emoji_1: str
    character_emoji_2: str

    name: str
    description: str
    special_ability_1: OllamaSpecialAbilityModel
    special_ability_2: OllamaSpecialAbilityModel
    special_ability_3: OllamaSpecialAbilityModel
    special_ability_4: OllamaSpecialAbilityModel
