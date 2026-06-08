import enum
from pydantic import BaseModel, Field, ConfigDict


class AbilityTarget(enum.Enum):
    SELF = "self"
    OTHER = "other"
    MULTI = "multi"

class OllamaSpecialAbilityModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    target: AbilityTarget
    range: int = Field(..., ge=0, le=10)
    area_of_effect: int = Field(..., ge=0, le=10)

    health_add: int = Field(ge=-10, le=10)
    defense_add: int = Field(ge=-10, le=10)
    movement_add: int = Field(ge=-10, le=10)
    attack_power_add: int = Field(ge=-10, le=10)
    will_stun: bool

class OllamaCharacterDefinitionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    special_ability_1: OllamaSpecialAbilityModel
    special_ability_2: OllamaSpecialAbilityModel
    special_ability_3: OllamaSpecialAbilityModel
    special_ability_4: OllamaSpecialAbilityModel
